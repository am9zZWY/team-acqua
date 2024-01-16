# Assessing the Blue Planet: A Comprehensive Study of Global Water Resources

## Getting started

### Prepare the environment

Create and activate a virtual environment:

```
python3 -m venv env
source env/bin/activate
```

Install the required packages:

```
pip install -r requirements.txt
```

---

**Important:**

Make sure that your IDE uses the virtual environment.
In PyCharm, for example, you can set the Python interpreter in `Settings > Project > Project Interpreter`.
The interpreter for the virtual environment is located in `env/bin/python`.

---

### Deactivate the environment

```
deactivate
```

## Plan

Question 1: "Which regions are mostly affected by climate change in terms of renewable water availability?":

1. Analyse the precepitation data
   WHY: because water availability is likely linked to rainfall
   Find some literature that shows that this is true
   We don't have to took at total exploitable water resources since we _know_ that rain might be one of the biggest
   exploitable water resources
    1. plot spatial data as global plot
       -> Rainfall did not decline but its distribution changed over time
    2. identify regions where the precepitation is low
       -> these are regions that are likely to be affected by water scarcity

Question 2: "Which water management strategies (Maßnahmen) are used by regions with different levels of water stress?"

1. Plot which water management strategies are used globally
    -> look at all water management strategies for each country and plot the proportion of the strategy
2. Compare countries which are mostly affected by water scarcity to the global trend
   3. Nullhypothesis: "There's no difference in water management strategies between country that are affected by water scarcity and the global trend."
   4. Regression: Water Scarcity als Input -> Water Treatment als Output, gibt es einen Regressionsgrad: -> "Je höher die Scarcity, desto höher derdiedas Water Treatment".
   3. Zonen-Einteilung mithilfe von ANOVA -> mehr kategorisiert.
   4. Plot one side the global trend and on the side a result of  

1. Select countries that are similar (e.g., same pop or same water withdrawal) to each other
    and differ in water stress
2. Short overview over the similarities of the two regsions
3. Compare different water management strategies
    -> it's ok to look at only one year of water management strategies

Plot 3: Water Withdrawal on one axis and 


2. Water Withdrawal and Agriculture and Industry
   -> it would be interesting to see if there are regions that are affected by water scarcity and where the water
   withdrawal is high
    1. 
