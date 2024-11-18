use std::{fmt, sync::Arc};

/// Type used for when a fact match is found
pub type DuplicateFactMatch = (Fact, Fact, f64);
/// Wagner-Fishcer similarity threshold
pub const SIMILARITY_THRESHOLD: f64 = 82.5;

/// The classification of a Fact, safe or unsafe
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FactClass {
    Safe,
    Unsafe,
}

/// Struct holding information about a fact in a fact file
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Fact {
    /// The fact text
    pub fact: Arc<String>,
    /// The class of the fact (safe or unsafe)
    pub class: FactClass,
    /// The line number of the fact in it's respective file
    pub line_number: usize,
}

impl Fact {
    pub fn new(fact: String, class: FactClass, line_number: usize) -> Self {
        Self {
            fact: Arc::new(fact),
            class,
            line_number,
        }
    }
}

impl fmt::Display for FactClass {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FactClass::Safe => write!(f, "Safe"),
            FactClass::Unsafe => write!(f, "Unsafe"),
        }
    }
}
