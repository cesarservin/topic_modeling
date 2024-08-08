topic_modeling
==============
![topic_modeling_Logo.jpg](img/topic_modeling_Logo.jpg#only-light)

## Usage
- **Basic Usage**: Run `topic_modeling.exe` or use `topic_modeling_main.ipynb`
- **Configuration**: Modify pyproject.toml to add or remove packages.

## Data
- **Sources**: The dataset is collected by CPG distributor public site.
- **Structure**: Table of key features

!!! example
    Input data format

| Text      | 
| :-------- |
| `string`  |


## Result ✅
 - **Findings:**
   - Based on the model the results of topics and words are different. This is not surprising as these methods are using different approaches under the hood.

      Overall, I would prefer to go with the LDA method as is has been a well stablished methodn on this field.

- **Visualizations**:
  - Example visualizations (if applicable).
  ![output_results.jpg](img/output_results.jpg)

Directory Structure
==============

    .
    ├── docs <- markdown files for mkdocs
    │   └── img <- assets
    ├── notebooks <- jupyter notebooks for exploratory analysis and explanation
    └── src - scripts for processing data eg. transformations, dataset merges etc.
    │   ├── data <- loading, saving and modelling your data
    │   ├── features <- feature engineering
    │   ├── model <- algorithms and models
    │   ├── plots <- plots
    │   └── utils <- api and other
    ├── LICENSE <- License
    ├── mkdocs.yml <- config for mkdocs
    ├── pyproject.yml <- config project
    └── README.md <- README file of the package

## Contributing

To contribute create a PR a use conventional [commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)

```
fix: <description>
feat: <description>
docs: <description>
refactor: <description>
```

**License**

The project is licensed under the MIT License.

I hope this is helpful!