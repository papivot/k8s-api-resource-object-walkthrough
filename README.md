# A Simple Python Flask App to view Kubernetes Objects 

Are you tired of typing `kubectl get ....` ? Do you want to know which APIs are registered in your Kubernetes cluster, or all the API resources in your Kubernetes cluster? Want to view these using a handy browser UI? Then this is the solution for you!

Launched as a standalone app or executed from within a Kubernetes cluster, this app can make your life much easier. Access the application from a browser and filter through the various APIs, Resources, and Namespaces to view the complete details of various Kubernetes objects.



https://user-images.githubusercontent.com/47264956/148807623-4c381a45-67b8-4384-9dab-d9403d4258d9.mov



Main Menu - 

  ![](/images/main.png)

Use the provided filters to narrow your search results - 

- Select the API group (including core/v1)
  
  ![](/images/apigroup.png)

- Based on the API group selected, select the resource - 
  
  ![](images/resource.png)

- If Namespaced resource was selected in the previous option, select the relevent namespace -
  
  ![](images/namespace.png)

- Select the relavent object to get the details on it - 
  
  ![](images/object.png)

Get a detailed JSON output of the relavent object =
  
  ![](images/result.png)

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
