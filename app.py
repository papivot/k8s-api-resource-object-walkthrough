import os
import urllib3
import requests
from kubernetes import client, config
from kubernetes.client import configuration
from flask import Flask, render_template, jsonify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_kubeapi_request(httpsession, path,header):
    response = httpsession.get(path, headers=header, verify=False)
    if response.ok:
        response.encoding = 'utf-8'
        return response.json()
    else:
        return 0

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    k8s_host = ""
    k8s_token = ""
    k8s_headers = ""
    apis = dict()
    apis_dict = dict()

    # Connect to the Kubernetes cluster and grab a session id
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    # using the session ID, get all the APIs registered in the cluster
    apis = get_kubeapi_request(k8s_session,k8s_host+"/apis/",k8s_headers)
    if (apis):
        for values in apis["groups"]:
            apis_dict[values["preferredVersion"]["groupVersion"]] = values["name"]
        apis_dict["core/v1"] = "core"
        api_list = [(k,v) for k, v in apis_dict.items()]
        api_list.sort()      

    return render_template('index.html', api_list=api_list)

@app.route('/resource/<api>/<version>', methods=['GET','POST'])
def resource_route(api,version):

    apisresources = dict()
    resource_dict = dict()

    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        apisresources = get_kubeapi_request(k8s_session, k8s_host+"/api/v1", k8s_headers)    
    else:
        apisresources = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version, k8s_headers)
    
    if (apisresources):
        for values in apisresources["resources"]:
            if not ("/" in values['name']):
                resource_dict[values['name']] = values['namespaced']

    resource_list = [(k,v) for k, v in resource_dict.items()]
    resource_list.sort()

    return jsonify(resource_list)

@app.route('/namespace', methods=['GET','POST'])
def namespace_route():

    namespaces_list = []
    
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    # Using the session ID, get all the namespaces in the cluster
    namespaces = get_kubeapi_request(k8s_session,k8s_host+"/api/v1/namespaces",k8s_headers)
    if (namespaces):
        for values in namespaces["items"]:
            namespaces_list.append(values["metadata"]["name"])
        namespaces_list.append("*")
        namespaces_list.sort()
    return jsonify(namespaces_list)

@app.route('/obj/<api>/<version>/<resource>',methods=['GET','POST'])
def object_route(api,version,resource):
    
    obj_array = []
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        objects = get_kubeapi_request(k8s_session, k8s_host+"/api/v1/"+resource, k8s_headers)    
    else:
        objects = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version+"/"+resource, k8s_headers)
    
    if (objects):
        for values in objects["items"]:
            obj_array.append(values['metadata']['name'])
        obj_array.append("*")
        obj_array.sort()
         #return jsonify(objects['items'])
        return jsonify(obj_array)

@app.route('/namespaced-obj/<api>/<version>/<namespace>/<resource>',methods=['GET','POST'])
def ns_object_route(api,version,namespace,resource):
    
    ns_obj_array = []
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        objects = get_kubeapi_request(k8s_session, k8s_host+"/api/v1/namespaces/"+namespace+"/"+resource, k8s_headers)    
    else:
        objects = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version+"/namespaces/"+namespace+"/"+resource, k8s_headers)
    
    if (objects):
        for values in objects["items"]:
            ns_obj_array.append(values['metadata']['name'])
        ns_obj_array.append("*")
        ns_obj_array.sort()
    #    return jsonify(objects['items'])
        return jsonify(ns_obj_array)

@app.route('/objdetail/<api>/<version>/<resource>',methods=['GET','POST'])
def objectdetail_route(api,version,resource):
    
    obj_array = []
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        objects = get_kubeapi_request(k8s_session, k8s_host+"/api/v1/"+resource, k8s_headers)    
    else:
        objects = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version+"/"+resource, k8s_headers)
    
    if (objects):
        return jsonify(objects['items'])

@app.route('/namespaced-objdetail/<api>/<version>/<namespace>/<resource>',methods=['GET','POST'])
def ns_objectdetail_route(api,version,namespace,resource):
    
    ns_obj_array = []
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        objects = get_kubeapi_request(k8s_session, k8s_host+"/api/v1/namespaces/"+namespace+"/"+resource, k8s_headers)    
    else:
        objects = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version+"/namespaces/"+namespace+"/"+resource, k8s_headers)
    
    if (objects):
        return jsonify(objects['items'])

@app.route('/individualobjdetail/<api>/<version>/<resource>/<objname>',methods=['GET','POST'])
def individual_objectdetail_route(api,version,resource,objname):
    
    obj_array = []
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        objects = get_kubeapi_request(k8s_session, k8s_host+"/api/v1/"+resource+"/"+objname, k8s_headers)    
    else:
        objects = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version+"/"+resource+"/"+objname, k8s_headers)
    
    if (objects):
        return jsonify(objects)

@app.route('/individualnamespaced-objdetail/<api>/<version>/<namespace>/<resource>/<objname>',methods=['GET','POST'])
def individualns_objectdetail_route(api,version,namespace,resource,objname):
    
    ns_obj_array = []
    if not os.environ.get('INCLUSTER_CONFIG'):
        config.load_kube_config()
    else:  
        config.load_incluster_config()

    k8s_host = configuration.Configuration()._default.host
    k8s_token = configuration.Configuration()._default.api_key['authorization']
    k8s_headers = {"Accept": "application/json, */*", "Authorization": k8s_token}
    k8s_session = requests.session()

    if (api == 'core'):
        objects = get_kubeapi_request(k8s_session, k8s_host+"/api/v1/namespaces/"+namespace+"/"+resource+"/"+objname, k8s_headers)    
    else:
        objects = get_kubeapi_request(k8s_session, k8s_host+"/apis/"+api+"/"+version+"/namespaces/"+namespace+"/"+resource+"/"+objname, k8s_headers)
    
    if (objects):
        return jsonify(objects)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')