
 # BetterMemorySugarBot
 [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
 [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

 **Now you will not forget about next infusion set or CGM sensor change! This app remembers for you!**
 ##### *__do it yourself__ project*

# Table of contents
 * [How does it work?](#how-does-it-work)
 * [Bugs, new features and questions](#bugs-new-features-or-questions)
 * [Instalation](#instalation)
   * [Fork project on Github](#fork-project-on-github)
   * [Deploy app to heroku](#deploy-app-to-heroku)
 * [Configuration](#configuration)
   * [Configurate atrigger](#atrigger-configuration)
   * [Configurate your notifications](#notifications)
     * [Filling in configuration form](#filling-in-configuration-form-on-heroku)
 * [Notifications](#notifications)
 * [IFTTT Applets tutorials](#ifttt-applets-tutorials)
    * [Facebook Messenger notifications](#facebook-messenger)
    * [push notifications](#push-notifications) from IFTTT mobile app
    * [email](#email-notifications)
 * [Logging in to your website](#logging-in-to-your-website)
 * [**Turn your app on**](#turn-it-on)
 * [Update my site](#update-my-site)


# How does it work?
 1. every day at given time - atrigger.com automatically triggers your website
 2.  BetterMemorySugarBot automatically reads last change data from your [nightscout](https://github.com/nightscout/cgm-remote-monitor) website
 3. BetterMemorySugarBot calculates your next change date
 4.  BetterMemorySugarBot notifies you via IFTTT or SMS about remaing hours to approaching change. Read more about notifications [here](#notifications)

# Bugs new features or questions
You discovered some bug ?? Need some new feature? Have a question? Or maybe, you just need little help during instalation process or further usage ? Feel free to [create a new issue](https://github.com/Simon-the-Shark/BetterMemorySugarBot/issues/new)

# Instalation
1. [Fork project on Github](#fork-project-on-github)
2. [Deploy app to heroku](#deploy-app-to-heroku)
3. [Configurate](#configuration)

### Fork project on Github
 1. [Create Github account](#creating-github-account) or [log in](https://github.com/login) if you had already one.
 2. Go to [this project page](https://github.com/Simon-the-Shark/BetterMemorySugarBot). (you are probably already here)
 3. Click `Fork` button. (picture below)
 ![doc5](/readme-images/doc5.png)
4. Click `F5` on your keyboard to refresh website.
5. You have your own fork of repository now. Since now, do all instructions there.

### Creating Github account
1. Go to this [link](https://github.com/join?source=header-home)
2. Fill in the form and verify your humanity. Click `Create an account` button. (example picture below)
![doc1](/readme-images/doc1.png)
3. Choose free plan (default) and click `Continue` button. (picture below)
![doc2](/readme-images/doc2.png)
4. Click `skip this step` button. (picture below)
![doc3](/readme-images/doc3.png)
5. Verify your email addres (example picture below)
![doc4](/readme-images/doc4.png)

### Deploy app to Heroku
1. Make sure you are in **YOUR forked repositorium** (not in original one). Read about forking [here](#fork-project-on-github)
1. Click

    [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Create Heroku account.  New account is highly recomended by me, because of heroku`s free dynos(read more [here](https://devcenter.heroku.com/articles/free-dyno-hours)).
   * Fill in registration form (example picture below)
   ![doc6](/readme-images/doc6.png)
   * Confirm your email addres. (example picture below)
   ![doc7](/readme-images/doc7.png)
   * Set your password and click `SET PASSWORD AND LOG IN` button.
   * Click `CLICK HERE TO PROCEED` button.
3. [Fill in configuration form](#filling-in-configuration-form-on-heroku)
4. Click `Deploy app` button.
5. Watch building logs
6. Now you should see view like this:
  ![doc13](/readme-images/doc13.png)
7. Your app is properly deployed. Instalation process is over. Now time for [configuration](#configuration).

### Filling in configuration form on Heroku
example picture on bottom of this tab
**FIELDS:**
- **required**:
    * `App name` and `app_name` - first of all, I apologize for duplication, but it is necessary. It`s unique name of your app. It will be used in website URL (https://<app_name>.herokuapp.com). Please make sure, that this two fields are equal.
    * `heroku_token` - your unique token on heroku. Go to [this intructions](#heroku-token) in order to find out how to get it.
    * `LANGUAGE_CODE` - language of your app. Only accepted vaues are `en` (english)(default) or `pl` (polish).
    * `SECRET_KEY` - secret password for your app. Keep it in secret!! It will be used for authorization.
- ###### **settable later**:
  * `ATRIGGER_KEY` and `ATRIGGER_SECRET` - read more in [atrigger](#atrigger-configuration) section
  * `INFUSION_SET_ALERT_FREQUENCY` - amount of time beetwen infusion set changes. [in **hours**]
  * `NIGHTSCOUT_LINK` - http link to your nightscout website
  * `SENSOR_ALERT_FREQUENCY` - amount of time beetwen CGM sensor changes. [in **hours**]
![doc11](/readme-images/doc11.png)
![doc12](/readme-images/doc12.png)

### heroku token
heroku token is your unique API key.
**getting instructions**:
1. Go to [this link](https://dashboard.heroku.com/account)
2. Scroll down to `API Key` section (picture below)
3. Click `Reveal` button
4. Now you know your heroku token. **COPY** it and **PASTE** it to [`heroku_token` field](#filling-in-configuration-form-on-heroku)
![doc10](/readme-images/doc10.png)

# Configuration
 1. [Configurate atrigger](#atrigger-configuration)
 2. [Configurate your notifications](#notifications)


### atrigger configuration
1. go to [this link](https://atrigger.com/user/register)
2. Fill in registration form and click `Create My Account` button (if had not already done this). (example picture below)
 ![doc14](/readme-images/doc14.png)
3. Now you should see page like below. (if you are not just go to [this link](http://atrigger.com/panel/setup))
![doc15](/readme-images/doc15.png)
4. On the picture above, I have marked `API Key` and `API Secret`. You can copy and paste them into [configuration form in instalation process](#filling-in-configuration-form-on-heroku) or set it when your app had been already deployed. (see [this instructions](#atrigger_key-and-atrigger_secret-setting))
5. [Verify atrigger with ATriggerVerify.txt](#atriggerverify.txt)
6. Now you can go back to [configuration instructions](#configuration).
##### `ATRIGGER_KEY` and `ATRIGGER_SECRET` setting
1. In order to find out how to get them, go [here](#atrigger-configuration)
2. If you already had them, time for [logging in to your website](#logging-in-to-your-website)
4. Now you should see a page like below. Now you can paste your `ATRIGGER_KEY` in right field and click `CHANGE` button.
![doc18](/readme-images/doc18.png)
5. You should see a green confirmation like below
![doc19](/readme-images/doc19.png)
6. Now you can paste your `ATRIGGER_SECRET` in right field and click `CHANGE` button. You should see similar green message. (example picture below)
![doc20](/readme-images/doc20.png)
7. Now your `ATRIGGER_KEY` and `ATRIGGER_SECRET` are set. Go back to [atrigger configuration](atrigger-configuration).

### ATriggerVerify.txt
1. Go to [atrigger setup website](https://atrigger/panel/setup) and download verification file. (picture below)
![doc21](/readme-images/doc21.png)
2. Now [log in to your website](#logging-in-to-your-website)
3. You should see page like below. Click gray `Upload verification file` button.
![doc22](/readme-images/doc22.png)
4. Click `Choose file` button and choose your ATriggerVerify.txt from your computer. (picture below)
![doc23](/readme-images/doc23.png)
5. Click `UPLOAD` button. (picture below)
![doc24](/readme-images/doc24.png)
6. You should see green sucess message like below.
![doc25](/readme-images/doc25.png)

# Logging in to your website
1. Go to your website (https://`<app_name>`.herokuapp.com). You should see page like below. Now click `IT IS MYWEBSITE` buttton.
![doc16](/readme-images/doc16.png)

2. Now type your `SECRET_KEY` (it has been set during [instalation process](#filling-in-configuration-form-on-heroku)) and click `LOG IN` button. (example picture below)
![doc17](/readme-images/doc17.png)
3. You are logged in !


# Notifications
**BetterMemorySugarBot** has two ways of notifying. I recomend notifying via **IFTTT**. It`s completly free, easier to set up and it is flexible. You can choose notifying via **facebook messenger**, **push notifications** from mobile app or **email**. Of course, you can explore this platform and combine BetterMemorySugarBot with other services on your own.Second options is **SMS via Twilio API**. I have to warn you, that **when free credits are run out, you will have to pay for text messages**. To use your free credits you do not have to give them any credit card or any other billing info. It is also a little more complicated to configurate than IFTTT. If you had decided, you can go to [notifications configuration instruction](#notifications-configuration-instructions)

### Notifications configuration instruction
1. [Log in to your website](#logging-in-to-your-website) and go to menu view.
2. Choose your notification time (custom time when notification occures). **PLEASE TYPE [UTC TIME](https://www.timeanddate.com/time/map/)**. Click `CHANGE`. *Default value is 16 (UTC)*.
![doc67](/readme-images/doc67.png)
2. Go to notifications center.
![doc26](/readme-images/doc26.png)
3.  Choose your notifications way (you can choose both) and click `CHANGE` button. (picture below)
![doc27](/readme-images/doc27.png)
4. Now go to [IFTTT configuration](#ifttt-configuration) or to [SMS configuration](#sms-configuration)


### IFTTT configuration
1. If you are here, I assume you had already followed [notifications configuration instruction](#notifications-configuration-instructions)
2. Create account on IFTTT or if you already done this, you can [log in](https://ifttt.com/login?wp_=1)
   * Go to [this link](https://ifttt.com)
   * You can sign up with your social media account or just type your email and click `Get started` button.
   * If you had choose email registration, now type your password and click `Sign up` button.
3. Now go to [this link](https://ifttt.com/services/maker_webhooks)
4. Click `Connect` button (picture below)
![doc29](/readme-images/doc29.png)
5. Click `Documentation` button (picture below)
![doc30](/readme-images/doc30.png)
6. Copy your key. (picture below)
![doc31](/readme-images/doc31.png)

7. Now [log in to your website](#logging-in-to-your-website) and go to notifications center. You should see page like below.
![doc32](/readme-images/doc32.png)

8. Click `MANAGE IFTTT MAKERS` button (picture above)
9. Now paste your `IFTTT key` and click `ADD` button. (picture below)
![doc33](/readme-images/doc33.png)

10. Now you should see green message. (picture below)
![doc34](/readme-images/doc34.png)

11. Of course, you can add more IFTTT accounts and BetterMemorySugarBot will trigger all of them.
12. Finally, time for creating your own notifying applet:
    * [Facebook Messenger notifications](#facebook-messenger)
    * [push notifications](#push-notifications) from IFTTT mobile app
    * [email](#email-notifications)
    * explore IFTTT and create some other custom applet
### IFTTT Applets tutorials
### Facebook Messenger
1. Go to [this link](https://ifttt.com/create)
2. Click `+this` button. (picture below)
![doc35](/readme-images/doc35.png)
3. Search for `webhooks` and click it. (picture below)
![doc36](/readme-images/doc36.png)
4. Click `Receive web request` (picture below)
![doc37](/readme-images/doc37.png)
5. Type
    >`sugarbot-notification`

    and click `Create trigger` button. (picture below)
![doc38](/readme-images/doc38.png)
6. Click `+that` button. (picture below)
![doc39](/readme-images/doc39.png)
7. Search for
     >messenger

    and click `Facebook Messenger` button. (picture below)
![doc40](/readme-images/doc40.png)
8. Click `connect` button. (picture below)
![doc41](/readme-images/doc41.png)
9. Log in to your Facebook account

![doc42](/readme-images/doc42.png)

10. Click `Get Started` button. (picture below)
![doc43](/readme-images/doc43.png)

11. You should see something like below

![doc44](/readme-images/doc44.png)

12. Confirm your connection via link in your email box.(example picture below)
![doc45](/readme-images/doc45.png)
13. Now get back to your applet creation site.
14. Click `Send message` button.  (picture below)
    * if do not see the same, just click `back` and repeat 7th step from this instruction
![doc46](/readme-images/doc46.png)
15. In `Message text` field paste:
    >{{Value1}}
16. Click `Create action` button. (picture below)
![doc47](/readme-images/doc47.png)
17. Click `Finish` button and now your applet is ready.
18. If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, you are ready to [turn this app on](#turn-it-on) !!!

### Push Notifications
1. Go to [this link](https://ifttt.com/create)
2. Click `+this` button. (picture below)
![doc35](/readme-images/doc35.png)
3. Search for `webhooks` and click it. (picture below)
![doc36](/readme-images/doc36.png)
4. Click `Receive web request` (picture below)
![doc37](/readme-images/doc37.png)
5. Type
   >sugarbot-notification

6. click `Create trigger` button. (picture below)
![doc38](/readme-images/doc38.png)
6. Click `+that` button. (picture below)
![doc39](/readme-images/doc39.png)
7. Search for
     >notifications

   and click `Notifications` button. (picture below)
![doc48](/readme-images/doc48.png)
8. Click `connect` button. (picture below)
![doc49](/readme-images/doc49.png)
14. Click `Send notifications from the IFTTT app` button.  (picture below)
![doc50](/readme-images/doc50.png)
15. In `Message` field paste:
    >{{Value1}}
16. Click `Create action`` button. (picture below)
![doc58](/readme-images/doc58.png)
17. Click `Finish` button and now your applet is ready.
18. Now you just have to download IFTTT app and log in to your account. IFTTT asks you for your number. You can give it them and they will send you a link or just download it from [Google Play](http://ift.tt/google-play-download) or [App Store](http://ift.tt/app-store-download)
18. If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, you are ready to [turn this app on](#turn-it-on) !!!

### Email notifications
1. Go to [this link](https://ifttt.com/create)
2. Click `+this` button. (picture below)
![doc35](/readme-images/doc35.png)
3. Search for `webhooks` and click it. (picture below)
![doc36](/readme-images/doc36.png)
4. Click `Receive web request` (picture below)
![doc37](/readme-images/doc37.png)
5. Type
   >sugarbot-notification

6. click `Create trigger` button. (picture below)
![doc38](/readme-images/doc38.png)
6. Click `+that` button. (picture below)
![doc39](/readme-images/doc39.png)
7. Search for
     >email

   and click `email` button. (picture below)
![doc51](/readme-images/doc51.png)
8. Click `connect` button. (picture below)
![doc52](/readme-images/doc52.png)
9. Type your email and click `Send PIN` button.  (picture below)
![doc53](/readme-images/doc53.png)
10. Go to your email box and copy your PIN. Paste it in `PIN` field. (picture below)
 ![doc54](/readme-images/doc54.png)
11. Click `Connect` button.
12. Now get back to your applet creation site.
14. Click `Send me an email` button.  (picture below)
![doc55](/readme-images/doc55.png)
14. In `Subject` field, type your custom message subject e.g. *"BetterMemorySugarBot Notification"*
15. In `Body` field paste:
    >{{Value1}}
16. Click `Create action` button. (picture below)
![doc59](/readme-images/doc59.png)
17. Click `Finish` button and now your applet is ready.
18. If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, you are ready to [turn this app on](#turn-it-on) !!!

### SMS configuration
This tutorial will be avaible soon. Do you really need it?? [Let me know](#bugs-new-features-or-questions)!

# Turn it on
If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, your app is fully prepared for this final step.
1. [Log in to your website](#logging-in-to-your-website)
2. Click `SEND NOTIFICATION NOW` green button. (picture below)
![doc56](/readme-images/doc56.png)
3. You should see page similar to below one
![doc57](/readme-images/doc57.png)
4. **Congratulations !!!** Your app is working. Your first notifications has been sended ! Now every day at give time, BetterMemorySugarBot will send you a notification with remaing time. If you wants to check remaing time without notification, just click `QUIET CHECKUP` button in menu.

# Update my site
To check, if your site is up-to-date or not you should go to your forked repo.
1. Now look for message
    > This branch is `<some number>` commits behind Simon-the-Shark:master.
    (picture below)
![doc60](/readme-images/doc60.png)
2. If there is no message like this, your website is up-to-date
3. If you can see the message, your website needs to be updated. Follow the instructions below.
4. Click `Compare` button
![doc61](/readme-images/doc61.png)
5. Click `switching the base`
![doc62](/readme-images/doc62.png)
6. You should see page similar to below. Click `Create pull request` button
![doc63](/readme-images/doc63.png)
7. Now click green `Merge pull request` button
![doc64](/readme-images/doc64.png)
8. Type short description and click `Confirm merge button` (example picture below)
![doc65](/readme-images/doc65.png)
9. Now message in your repository should contain `ahead` word
![doc66](/readme-images/doc66.png)


