use pyo3::prelude::*;
use std::{
    process::Command,
    path::PathBuf,
    io::{BufReader, BufRead},
    fs::File,
};
use itertools::Itertools;
use indicatif::ProgressBar;


fn lines_from_file(filename: &PathBuf) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

// #[pyfunction]
fn main() {
    // get project's top level
    let output = Command::new("git")
        .args(&["rev-parse", "--show-toplevel"])
        .output()
        .expect("failed to execute git process");

    if !output.status.success() {
        panic!("Error:  {}", String::from_utf8_lossy(&output.stderr));
    }

    // read safe.txt and unsafe.txt into lists
    let mut project_root: PathBuf = PathBuf::from(String::from_utf8(output.stdout).unwrap().trim());
    project_root.push("randfacts");
    project_root.push("safe.txt");

    let mut all_facts = lines_from_file(&project_root);


    project_root.pop();
    project_root.push("unsafe.txt");

    let mut unsafe_contents = lines_from_file(&project_root);

    all_facts.append(&mut unsafe_contents);

    // Generate all possible pairs of the facts from safe.txt and unsafe.txt
    // combined
    let mut matches: Vec<String> = vec![];
    let pb = ProgressBar::new(num_integer::binomial(all_facts.len() as u64, 2));
    let combinations = all_facts.into_iter().combinations(2);
}

// #[pymodule]
// fn checkdups(_py: Python, m: &PyModule) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(main, m)?)?;
//     Ok(())
// }