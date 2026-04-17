<div align="center" markdown="1">

<a href="https://frappe.io/products/cafe">
    <img src=".github/logo.svg" height="80" alt="Frappe Cafe Logo">
</a>

<h1>Cafe</h1>

**Professional networking, minus the noise**

</div>

## Cafe
Cafe is a professional networking platform built on top of Frappe Framework to publish long-form insights and connect with like-minded individuals.

## Getting Started (Development)

### Local Setup

1. [Setup Bench](https://docs.frappe.io/framework/user/en/installation).
1. In the frappe-bench directory, run `bench start` and keep it running.
1. Open a new terminal session and cd into `frappe-bench` directory and run following commands:
    ```sh
    $ bench get-app builder
    $ bench get-app cafe
    $ bench new-site sitename.localhost --install-app cafe
    $ bench browse sitename.localhost --user Administrator
    ```
1. Access the cafe page at `sitename.localhost:8000/cafe` in your web browser.

