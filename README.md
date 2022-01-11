# A Simple Python Flask App to view Kubernetes Objects 

Are you tired of typing `kubectl get ....` ? Do you want to know which APIs are registered in your Kubernetes cluster, or all the API resources in your Kubernetes cluster? Want to view these using a handy browser UI? Then this is the solution for you!

Launched as a standalone app or executed from within a Kubernetes cluster, this app can make your life much easier. Access the application from a browser and filter through the various APIs, Resources, and Namespaces to view the complete details of various Kubernetes objects.

Watch the video 

[![Watch the video](/images/screenshot.png)](https://youtu.be/7gkSOYGfK_Y)

## Executing as a standalone Python app

- Clone this repository.
- Make sure that Python3 is installed on the host.
- Use `pip3` to install the required dependencies (if not already installed) `pip3 install -r ./requirements.txt`
- A working `KUBECONFIG` file with a valid `context` is accessible.
- Execute the python app - `python app.py`
- Access the app using the browser at `http://IP_ADDRESS_OF_HOST:5000`

## Building a new container image (optional)

- Clone this repository.
- Use the provided Dockerfile as a sample and build a new container image. 
- Upload the image to a registry of your choice

## Deployment on a K8s cluster (preferred method) 

- Use the attached `Dockerfile` to build a new container image or use one already referenced in the sample deployment YAML.
- Use the sample `kubernetes-deployment/deployment.yaml` to deploy the application. Modify the `kubernetes-deployment/deployment.yaml` file as per requirements -
  - Ensure that the `INCLUSTER_CONFIG` env variable is set to 1. 
  - Modify the `image: whoami6443/k8sapiwalkthru:x.y.z` to a valid value if using a custom-built image. 
- Deploy the application - `kubectl apply -f kubernetes-deployment/deployment.yaml`
- Access the application using a browser, using the IP address of the service `k8s-papivot-tools-svc`. 
- The application can also be exposed using a method of your choice - e.g., Istio, Ingress, Gateway, etc. 
