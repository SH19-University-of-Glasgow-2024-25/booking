# Hosting

This document aims to provide the reader with enough information to run the platform on a simple EC2 instance.

What do you need to follow this guide?
- A configured Amazon Web Services account.
- A GitHub account with access to the platform's repository.
- A Windows command prompt.
- The URL for downloading your repository via SSH.
- Production environment file/variables.

## Creating your EC2 instance.

Follow only Step 1 of the AWS provided guide on how to create an EC2 instance [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html). 
Note,
- use the `(Europe) Ireland` region.
- use the Amazon Linux OS image.
- use the instance type t2.micro.
## Setting up the platform.

Next, you must SSH into your EC2 instance.
- Open your command prompt
- Run the following `ssh -i <your-key> ec2-user@<EC2-IPv4>`
- Clone the repository using `git clone git@<repository-ssh>`
- Change directory to your repository using `cd <repository-name>`
- Install docker using the following commands
    - `sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m) -o /usr/local/bin/docker-compose`
    - `sudo chmod +x /usr/local/bin/docker-compose`
- To verify installation use `docker-compose --version`, you should expect an output similar to `Docker Compose version <version-number>`

- Run `sudo docker-compose --env-file .env.prod -f docker-compose-prod.yml up`

Now your server is running anytime you connect to the IPv4 of your EC2 instance.

## Linking an EC2 Instance to a DNS Record and Setting Up SSL with Certbot  

This following explains how to link an **Amazon EC2 instance** to a **domain name** and secure it with an **SSL certificate** using **Certbot**.

### Step 1: Retrieve Your EC2 Public IP Address  

1. Log in to the **AWS Management Console**.  
2. Navigate to **EC2 > Instances**.  
3. Find your instance and copy its **public IPv4 address**.  

---

### Step 2: Configure Your DNS Provider  

Log in to your **DNS provider** (such as GoDaddy, Namecheap, or Cloudflare).  
You need to create **A Records** to map your domain to the EC2 instance's **public IP**.

- **For the root domain (`yourdomain.com`)**:  
  - **Type**: `A Record`  
  - **Host/Name**: `@` (or `yourdomain.com`)  
  - **Value**: `<IPv4-address>`  
  - **TTL**: Default (e.g., `300 seconds`)  

- **For the `www` subdomain (`www.yourdomain.com`)**:  
  - **Type**: `A Record`  
  - **Host/Name**: `www`  
  - **Value**: `<IPv4-address>`  
  - **TTL**: Default  

After making these changes, **wait for DNS propagation**, which can take anywhere from a few minutes to a few hours.  

To get SSL on your server follow the instuction at [certbot](https://certbot.eff.org/)