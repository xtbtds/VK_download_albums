# Download photo albums from VK.

# Method 1

0. You need to be authorized in vk.com.

1. To get token follow the link: https://oauth.vk.com/authorizeclient_id=51526963&redirect_uri=https://oauth.vk.com/blank.html&callback&scope=30&display=mobile&response_type=token&v=5.89

2. Then, you'll be asked to give the app access to your profile information.

3. Copy the string between `access_token=` and `&expires_in=`, it is your token

4. Run `main.py`

5. Note that your token expires in 24 h. After that, you'll have to create a new one using the link from step 2.

# Method 2

0. You need to be authorized in vk.com.

1. Create a standalone-application here: https://vk.com/apps?act=manage. Copy your App ID:
<p float="left">
  <img src="imgs/vk2.png" width="500" />
</p>

2. To get token follow the link using your App ID: https://oauth.vk.com/authorizeclient_id=YOUR_APP_ID&redirect_uri=https://oauth.vk.com/blank.html&callback&scope=30&display=mobile&response_type=token&v=5.89

3. Copy the string between `access_token=` and `&expires_in=`, it is your token

4. Run `main.py`

5. Note that your token expires in 24 h. After that, you'll have to create a new one using the link from step 2.
