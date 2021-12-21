use pyo3::prelude::*;
use pyo3::create_exception;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn parse(code: String) -> PyResult<Vec<char>> {
    let code_vector: Vec<char> = code.chars().filter(|&n| n == '>' || n == '<' || n == '+' || n == '-' || n == '[' || n == ']' || n == '.' || n == ',').collect();
    //parse(code_vector);
    Ok(code_vector)
}


#[pyfunction]
pub fn compile(code: Vec<char>) -> PyResult<(String, Vec<u8>)> {
    let mut memory: Vec<u8> = vec![0; 30000];
    let mut mem_ptr: usize = 0;
    let mut code_ptr: usize = 0;
    let mut bracket_idx: Vec<usize> = Vec::new();
    let mut output: Vec<u8> = Vec::new();

    while code_ptr < code.len() { 
        let command = code[code_ptr]; 

        match command { 
            '+' => memory[mem_ptr] = memory[mem_ptr].wrapping_add(1),
            '-' => memory[mem_ptr] = memory[mem_ptr].wrapping_sub(1),
            '>' => mem_ptr += 1,
            '<' => mem_ptr -= 1, 
            '.' => output.push(memory[mem_ptr]),   
            '['=> bracket_idx.push(code_ptr), 
            ']'=> { 
                if memory[mem_ptr] != 0 {
                    code_ptr = *bracket_idx.last().unwrap()
                }
                else {
                    bracket_idx.pop();
                }
            }, 
            _ => println!("ERROR") 
        };
        code_ptr += 1;
    }
    //println!("{:?}", memory);
    let output:String = log_ptr(output);
    Ok((output, memory))
}

#[pyfunction]
fn log_ptr(byte: Vec<u8>) -> String { 
    let int_as_char: Vec<char> = byte.iter().map(|&n| n as char).collect();
    let output_as_str: String = int_as_char.into_iter().collect();
    return output_as_str.to_string();
}

/// A Python module implemented in Rust.
#[pymodule]
fn interpy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(compile, m)?)?;
    Ok(())
}
