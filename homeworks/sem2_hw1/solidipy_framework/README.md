<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Kynemallv/python_mipt_dafe/blob/main/homeworks/sem2_hw1/solidipy_framework/">
    <img src="https://github.com/Kynemallv/python_mipt_dafe/blob/main/homeworks/sem2_hw1/solidipy_framework/assets/images/logo.png?raw=true" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Solidipy-MIPT</h3>

  <p align="center">
    Make your ML solid!
    <br />
    <a href="https://github.com/Kynemallv/python_mipt_dafe/tree/main/homeworks/sem2_hw1/solidipy_framework/examples">Examples</a>
    ·
    <a href="https://github.com/Kynemallv/python_mipt_dafe/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Kynemallv/python_mipt_dafe/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<a id="about-the-project"></a>

## About The Project

*Solidipy-MIPT* is a Python library designed to provide a solid foundation for machine learning tasks. It includes various machine learning algorithms such as Weighted k-nearest neighbors (WKNN) and regressions, along with evaluation metrics to assess model performance.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a id="built-with"></a>

### Built With

Major frameworks/libraries used to bootstrap solidipy.

* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
<a id="getting-started"></a>

## Getting Started

To get a local copy up and running follow these simple example steps.

<a id="prerequisites"></a>

### Prerequisites

Before installing *Solidipy-MIPT* make sure you have last version of Python3 and pip.

<a id="installation"></a>

### Installation

You can install solidipy using pip:

```bash
pip install solidipy-mipt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
<a id="usage"></a>

## Usage

#### Simple Weighted KNN example
```python
import numpy as np
from solidipy_mipt import accuracy
from solidipy_mipt.algorithms import WKNN

X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
y = np.array([0, 1, 0, 1])
X_train, X_test, y_train, y_test = train_test_split(
  X, y, train_ratio=0.6, shuffle=True
)

wknn = WKNN()
wknn.fit(X_train, y_train)
prediction = wknn.predict(X_test)

print(accuracy(prediction, y_test))
```

_For more examples, please refer to the [solidipy_mipt examples](https://github.com/Kynemallv/python_mipt_dafe/tree/main/homeworks/sem2_hw1/solidipy_framework/examples)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<a id="contributing"></a>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
<a id="license"></a>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
<a id="contact"></a>

## Contact

Matvei Gorskii - [t.me/Kynemallv](https://twitter.com/your_username) - matveygor41@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
