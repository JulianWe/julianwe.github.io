# Create Virtual Machine on Google Cloud Platform

```sh
gcloud compute instances create gcp \
    --project=akash-456617 \
    --zone=us-central1-a \
    --machine-type=t2d-standard-1 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=ssh-keys=jw:ssh-ed25519\ \
AAAAC3NzaC1lZDI1NTE5AAAAIKTNqCzRZVoWV5hbr4yj\+mnV0ckEBfr68LC3BqZd3JsD\ jw \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=513538345283-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=ansible-1,disk-resource-policy=projects/akash-456617/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/ubuntu-os-cloud/global/images/ubuntu-2404-noble-amd64-v20250409,mode=rw,size=10,type=pd-standard \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
    --enable-nested-virtualization
```