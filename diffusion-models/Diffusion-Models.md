# Diffusion Models 

Diffusion models are a class of generative models in machine learning that create new data samples by simulating a process of adding noise to existing data and then learning to reverse that process.

These models have gained prominence in the realm of artificial intelligence starting with Dall-e specifically.
They largely gained traction for tasks like image generation, denoising, and inpainting. 

Diffusion models are inspired by physical processes, particularly the diffusion of particles in a medium, and competing with models like Generative Adversarial Networks (GANs) and Variational Autoencoders (VAEs).

## The Core Idea: How Diffusion Works
At a high level, diffusion models work by learning to reverse a process that gradually adds noise to data until it is completely random. But here's a step-by-step breakdown:

* **Forward Process (Noise Addition)**:

Starting from a real data point, such as an image, the model progressively adds noise(Gaussian) to it in multiple steps. This process transforms the original image into pure noise (usually Gaussian noise) over a series of steps.
At each step, a small amount of noise is added, making the data more and more random. After many steps, the original data is completely obscured by noise.

This process is mathematically modeled as a Markov chain, where each state depends only on the previous state13.

* **Reverse Process (Denoising)**:

The model then learns how to reverse this noising process—starting from random noise and gradually denoising it step by step, to recover the original data distribution.

The key idea is that by learning this reverse diffusion process, the model can generate new, previously unseen data points that resemble the original distribution.

This is conceptually similar to a physical process where particles diffuse over time, but instead of particles in space, we are diffusing data points in the "space" of possible images, text, or other data types.

Diffusion models operate based on probabilistic principles and can be described using latent variable models. They involve a sequence of transformations that map a simple distribution (like Gaussian noise) to a more complex distribution representative of the training data

## Training Diffusion Models
You need to teach the neural network what your target distribution is, let's say you want the NN to generate cartoons, you need to teach with a sample of cartoons, adding noise to them one step at a time and at each step, the model learns different features of the cartoons such as the outline, general details or anything in between.

You then reverse the noising and generate a cartoon so to say. You train the model to do this with each of your data sample, making it learn how to take different noisy images & turn them into cartoons you desire. 
The model learns how to remove the noise you added in the first place. Just like how adding noise is progressive and step by step, removing the noise to generate new images closer to target distribution is done progressively, step-by-step. 

* Loss Function: During training, the model learns to predict the added noise at each step of the diffusion process. By minimizing the difference between the predicted noise and the actual noise added during the forward process, the model improves its ability to reverse the noising process.
* Parameterization: The reverse process is often modeled as a neural network that predicts how to remove noise at each step, usually parameterized by a neural network like a U-Net architecture.

### Memory Requirements:

Due to the complex architecture and large number of parameters involved in training diffusion models, they can require significant memory resources, making them less accessible for resource-constrained environments.

### Sampling
During sampling, For the model to calculate and subtract the predicted noise, the model takes the input as a distributed noise image. After the first iteration, given the predicted noise is subtracted, the output is not exactly distributed 