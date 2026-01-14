<p align="center">
  <a href="https://github.com/txt/seai26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/seai26spr/blob/main/docs/lect/syllabus.md#top"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/19HJRraZex9ckdIaDHaTi0cGsvUcIhdTH6kIGoC_FODY/edit?gid=0#gid=0"><img 
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8118&bp=s"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/seai26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591 (013): Software Engineering and AI <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/seai26spr/main/docs/lect/banner.png"> 

# Review1

### **Topic 1: Data Representation & Pre-processing**

**1. Normalization (Min-Max)**

* **(a) [Understand]** Why is it algorithmically necessary to normalize data (scale 0..1) before calculating the distance between two rows?
* **(b) [Apply]** A dataset has a column "LinesOfCode" . A new module has 300 lines. Calculate its normalized score ().

**2. Handling Symbolic Data**

* **(a) [Recall]** In the class's CSV standard, how does the algorithm distinguish between a column of numbers and a column of symbols (e.g., "Gender")?
* **(b) [Analyze]** If you tried to calculate the "mean" of a symbolic column like `[Apple, Banana, Apple]`, it fails. What specific statistical transformation is used instead to represent the central tendency of symbols?

**3. The "Heaven" Point**

* **(a) [Recall]** Define the "Heaven" point in the context of multi-objective optimization (e.g., for a car with `MPG` and `Horsepower`).
* **(b) [Apply]** If we want to *minimize* weight (normalized 0..1) and *maximize* safety (normalized 0..1), what are the coordinate values of the "Heaven" point?

**4. Euclidean Distance**

* **(a) [Understand]** What does the Euclidean distance formula measure between a data row and the "Heaven" point?
* **(b) [Create]** Write the pseudocode or mathematical notation for calculating the distance  between a row  with  columns and the Heaven point .

**5. Data Headers & Goals**

* **(a) [Recall]** In the course CSV format, what does a `+` or `-` at the end of a column name indicate (e.g., `weight-`, `acceleration+`)?
* **(b) [Evaluate]** If a column has no `+` or `-` (e.g., `Age`), how should the optimization algorithm treat it compared to those that do?

---

### **Topic 2: Statistical Heuristics**

**6. Cohen’s Rule (Effect Size)**

* **(a) [Recall]** State the definition of a "small effect" according to Cohen’s rule in this class (formula involving Standard Deviation).
* **(b) [Apply]** Algorithm A has a mean score of 80. Algorithm B has a mean of 82. The Standard Deviation of the population is 10. Is the difference between A and B a "small effect" or a meaningful change? Show calculation.

**7. Standard Deviation (Variance)**

* **(a) [Understand]** What property of a dataset does Standard Deviation quantify?
* **(b) [Analyze]** In an optimization search, if the standard deviation of the current population drops to near zero, what does this indicate about the diversity of your solutions?

**8. Expected Values (Mode vs. Mean)**

* **(a) [Recall]** What is the "Expected Value" for a column of symbols?
* **(b) [Apply]** Given the list `[A, B, A, C, A, B]`, calculate the probability of the Expected Value.

**9. The "Half of You Die" Heuristic**

* **(a) [Understand]** Explain the recursive strategy described in class where "half the data is discarded" at each step.
* **(b) [Analyze]** Why is this logarithmic reduction () considered a "massive shortcut" compared to typical Deep Learning approaches?

**10. Sampling Validity**

* **(a) [Recall]** The lecturer claims we don't need to look at all data. What justification is given for using small samples (e.g., in the SQLite example)?
* **(b) [Evaluate]** If you only sample 100 points from a space of 3 billion, what assumption are you making about the "shape" of the solution space?

---

### **Topic 3: Optimization Algorithms**

**11. Genetic Algorithms: The Metaphor**

* **(a) [Recall]** In the "Mommy, Daddy, Kid" metaphor, what does the "Kid" represent in terms of data structures?
* **(b) [Apply]** If Parent A is `[1, 1, 1]` and Parent B is `[0, 0, 0]`, create a "Kid" using a single-point crossover at index 1.

**12. Mutation**

* **(a) [Understand]** What is the purpose of "mutation" in an evolutionary algorithm?
* **(b) [Analyze]** If you set the mutation rate to 0%, what risk does the algorithm face regarding "Local Optima"?

**13. Simulated Annealing**

* **(a) [Recall]** How does Simulated Annealing decide whether to accept a "worse" solution during the search?
* **(b) [Apply]** In the "breakfast" metaphor, if you only ever eat the "best" cereal you currently know, what are you missing out on? How does "temperature" solve this?

**14. Stochasticity**

* **(a) [Understand]** Why might running the same optimization code twice produce different results?
* **(b) [Evaluate]** If a manager complains that your code "isn't deterministic," how do you use the concept of Cohen's Effect Size to prove the two different results are effectively the same?

**15. Local vs. Global Optima**

* **(a) [Recall]** Define a "Local Optimum."
* **(b) [Analyze]** Why do greedy algorithms (that always take the best immediate step) often fail to find the Global Optimum?

---

### **Topic 4: Software Analytics & Research Concepts**

**16. Configuration Optimization (FLASH)**

* **(a) [Recall]** In the context of the SQLite case study, what was the goal of the optimization?
* **(b) [Apply]** If a system has 10 binary options (on/off), the search space is . If it has 50, it is . Explain why "brute force" testing is mathematically impossible for the second case.

**17. Transfer Learning**

* **(a) [Recall]** What is "Transfer Learning" in the context of software performance models (e.g., Valov et al.)?
* **(b) [Analyze]** If you train a model on "Data from 2020," why might it fail when tested on "Data from 2026"? What is this phenomenon called (often related to "Drift")?

**18. "Garbage In, Garbage Out" (Labeling)**

* **(a) [Understand]** How does the quality of labels (e.g., "Bug" vs "Not Bug") affect the "ceiling" of model performance?
* **(b) [Evaluate]** If it costs $50 to verify a label manually, and you have 10,000 instances, propose a strategy to build a model without spending $500,000.

**19. Multi-Objective Trade-offs**

* **(a) [Recall]** What does it mean when two goals are "conflicting" (e.g., Speed vs. Memory)?
* **(b) [Analyze]** If you find a solution that improves Speed by 50% but increases Memory usage by 200%, is this a "better" solution? How does the "Distance to Heaven" metric help decide?

**20. The "Less is More" Principle**

* **(a) [Recall]** What is the core technical argument of "Less is More" regarding model complexity?
* **(b) [Evaluate]** You have a Linear Regression model (Accuracy 90%) and a Deep Transformer model (Accuracy 91%). Using the course philosophy, which do you choose and why?
