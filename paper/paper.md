---
title: "pysolorie: a Python package for optimal orientation analysis of solar panels"
tags:
    - Python
    - astronomy
    - solar energy
    - solar panels
authors:
    - name: Alireza Aghamohammadi
      corresponding: true
      affiliation: 1
    - name: Amir Aghamohammadi
      affiliation: 2
    - given-names: M. Ebrahim
      surname: Foulaadvand
      affiliation: 3
affiliations:
    - name: Department of Computer Engineering, Sharif University of Technology, Tehran, Iran
      index: 1
    - name: Department of Fundamental Physics, Faculty of Physics, Alzahra University, Tehran, Iran
      index: 2
    - name:  Department of Physics, University of Zanjan, PC 45371-38791 Zanjan, Iran
      index: 3

date: 21 December 2023
bibliography: paper.bib
---

# Summary
How can one maximize the solar irradiation energy received by a fixed flat solar panel [@Aghamohammadi2023]? The orientation of a solar panel is determined by two angles: the tilt angle and the azimuthal angle [@Hafez2017].

![Orientational angles of a flat solar panel.\label{fig:opt}](solarpanel.svg)

**pysolorie** stands for **Py**thon **Sol**ar **Orie**ntation Analysis of Solar Panels. It is a Python package designed to help you find the optimal tilt angle of solar panels, $\beta$, to maximize the beam energy received for a given day. The optimal azimuthal angle is zero.

Its features include but are not limited to:

- Finding the optimal tilt angle for a fixed solar panel, assuming a clear-sky condition.
- Plotting the optimal tilt angle over a range of days.
- Plotting the daily direct irradiation energy over a range of days.
- Generating a CSV, JSON, or XML report detailing the optimal tilt angle over a range of days.
- Utilizing Hottel's model to quantify clear-sky conditions and estimate the atmospheric transmission of clear-sky beam radiation [@Hottel1976;@Iqbal1983].


# Statement of need
The amount of solar irradiation energy harvested by a solar collector depends on several factors. These include the time of irradiation (both the time of day and the day of the year), the latitude and climate of the location, and the shape and orientation of the solar panel [@Foulaadvand2023].
A solar collector can be positioned at a fixed orientation to maximize energy reception for a specific time period, such as daily, weekly, monthly, or seasonally, or it can be fixed for optimal performance throughout the year. The orientation can then be adjusted for the next time period.
Solar irradiation is composed of three components: the direct beam, sky diffusion, and ground reflection. For flat solar panels, we focus on direct beam irradiation, which contributes the most to solar irradiation. There are various models available for different climate types. We assume a clear sky condition with no clouds in the sky and an atmosphere free of pollutants. However, a cloudy sky or polluted air may affect the amount of solar energy received on Earth. There are some other issues which may require careful consideration and further investigation in future studies, such as panel efficiency, energy conversion, and the effects of air pollution.
 In our case, we use Hottel’s model to estimate the transmittance of direct solar radiation through a clear and sunny atmosphere [@Hottel1976;@AntonanzasTorres2019].

 With a well-defined, user-friendly, and extensible API, multiple audiences can benefit from `pysolorie`. These include solar energy researchers, solar panel manufacturers and installers, and instructors.

`pvlib python` is a library for simulating the performance of photovoltaic energy systems [@FHolmgren2018]. `pvlib python` implements two papers related to sun tracking [@Anderson2020;@Marion2013]. In the paper by Anderson & Mikofski,
the idea of backtracking and shading effect for a field of one-axis sun-trackers is discussed [@Anderson2020]. `pysolorie`, in contrast, considers a single flat-plate collector. This collector does not track the Sun and its orientation is optimally fixed. In the paper by Marion & Dobos, the optimal tracking angle for one-axis solar tracker is discussed [@Marion2013]. With the constraint of one-axis tracking, the incidence angle is minimized. However, `pysolorie` focuses on finding the optimal tilt angle for the solar panel, instead of sun tracking.

`Astropy` is the most well-known Python package with comprehensive functionality for astronomy and astrophysics [@Astropy2022]. It provides astronomical coordinate systems, cosmological calculations, and many more features. However, it lacks the ability to determine the optimal orientation of a flat solar panel, a feature that `pysolorie` provides.




# Background
The energy collected by a solar panel can be calculated using the formula in Equation \ref{eq:direct}, where:

- $n$ is the day of the year,
- $\phi$ is the latitude of the observer,
- $I(n)$ is the amount of extraterrestrial solar energy received per unit area per second [@Duffie2020;@Goswami2015]  on day number $n$ of the year,
- $\Omega$ is the Earth angular velocity around its axis with the value `7.15 * 1e-5` rad/s,
- $\theta$ is the angle between the position vector of the sun and the normal vector to the solar panel (incidence angle) [@Kalogirou2013],
- $\omega_s$ is the sunrise hour angle,
- $\omega_t$ is the sunset hour angle,
- $H$ is the Heaviside step function,
- $\tau_b$ is the beam atmospheric transmittance [@Hottel1976].

\begin{equation}\label{eq:direct}
E(n,\phi) = \frac{I(n)}{\Omega} \int_{\omega_s}^{\omega_t}\cos(\theta) \times H(\cos(\theta)) \times \tau_b~d\omega
\end{equation}

# Acknowledgements
 Amir Aghamohammadi would like to acknowledge the research council of the Alzahra University for the financial support.


# References
