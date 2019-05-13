
 # BetterMemorySugarBot
 [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
 [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Simon-the-Shark/BetterMemorySugarBot)

 **Now you will not forget about next infusion set or CGM sensor change! This app remembers for you!**
 ###### *__do it yourself__ project*

# Table of contents
 * [How does it work?](#how-does-it-work)
 * [Instalation](#instalation)
   * [Fork project on Github](#fork-project-on-github)
   * [Deploy app to heroku](#deploy-app-to-heroku)
 * [Configuration](#configuration)
   * [Configurate atrigger](#atrigger.com-configuration)
   * [Configurate your notifications](#notifications)
 * [Notifications](#notifications)
 * [IFTTT Applets tutorials](#ifttt-applets-tutorials)
    * [Facebook Messenger notifications](#facebook-messenger)
    * [push notifications](#push-notifications) from IFTTT mobile app
    * [email](#email-notifications)
 * [Logging in to your website](#logging-in-to-your-website)
 * [**Turn your app on**](#turn-it-on)


# How does it work?
 1. every day at given time - atrigger.com automatically triggers your website
 2.  BetterMemorySugarBot automatically reads last change data from your [nightscout](https://github.com/nightscout/cgm-remote-monitor) website
 3. BetterMemorySugarBot calculates your next change date
 4.  BetterMemorySugarBot notifies you via IFTTT or SMS about remaing hours to approaching change. Read more about notifications [here](#notifications)

# Instalation
1. [Fork project on Github](#fork-project-on-github)
2. [Deploy app to heroku](#deploy-app-to-heroku)
3. [Configurate](#configuration)

#### Fork project on Github
 1. [Create Github account](#creating-github-account) or [log in](https://github.com/login) if you had already one.
 2. Go to [this project page](https://github.com/Simon-the-Shark/BetterMemorySugarBot). (you are probably already here)
 3. Click `Fork` button. (picture below)
 ![]
4. Click `F5` on your keyboard to refresh website.

#### Creating Github account
1. Go to this [link](https://github.com/join?source=header-home)
2. Fill in the form and verify your humanity. Click `Create an account` button. (example picture below)
![]
3. Choose free plan (default) and click `Continue` button. (picture below)
![]
4. Click `skip this step` button. (picture below)
![]
5. Verify your email addres (example picture below)
![]

#### Deploy app to Heroku
1. Click

    [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Simon-the-Shark/BetterMemorySugarBot)
2. Create Heroku account.  New account is highly recomended by me, because of heroku`s free dynos.
   * Fill in registration form (example picture below)
   ![]
   * Confirm your email addres. (example picture below)
   ![]
   * Set your password and click `SET PASSWORD AND LOG IN` button.
   * Click `CLICK HERE TO PROCEED` button.
3. [Fill in configuration form](#filling-in-configuration-form-on-heroku)
4. Click `Deploy app` button.
5. Watch building logs
6. Now you should see view like this:
![]
7. Your app is properly deployed. Instalation process is over. Now time for [configuration](#configuration).

#### Filling in configuration form on Heroku
example picture on bottom of this tab
**FIELDS:**
- **required**:
    * `App name` and `app_name` - first of all, I apologize for duplication, but it is necessary. It`s unique name of your app. It will be used in website URL (https://www.<app_name>.herokuapp.com). Please make sure, that this two fields are equal.
    * `heroku_token` - your unique token on heroku. Go to [this intructions]() in order to find out how to get it.
    * `LANGUAGE_CODE` - language of your app. Only accepted vaues are `en` (english)(default) or `pl` (polish).
    * `SECRET_KEY` - secret password for your app. Keep it in secret!! It will be used for authorization.
- ###### **settable later**:
  * `ATRIGGER_KEY` and `ATRIGGER_SECRET` - read more in [atrigger](#atrigger.com-configuration) section
  * `INFUSION_SET_ALERT_FREQUENCY` - amount of time beetwen infusion set changes. [in **hours**]
  * `NIGHTSCOUT_LINK` - http link to your nightscout website
  * `SENSOR_ALERT_FREQUENCY` - amount of time beetwen CGM sensor changes. [in **hours**]


#### heroku token
heroku token is your unique API key.
**getting instructions**:
1. Go to [this link](https://dashboard.heroku.com/account)
2. Scroll down to `API Key` section (picture below)
3. Click `Reveal` button
4. Now you know your heroku token. **COPY** it and **PASTE** it to [`heroku_token` field](#filling-in-configuration-form-on-heroku)
![]
![]

# Configuration
 1. [Configurate atrigger](#atrigger.com-configuration)
 2. [Configurate your notifications](#notifications)


#### atrigger.com configuration
1. go to [this link](https://atrigger.com/user/register)
2. Fill in registration form and click `Create My Account` button (if had not already done this). (example picture below)
 ![]
3. Now you should see page like below. (if you are not just go to [this link](http://atrigger.com/panel/setup))
![]
4. On the picture above, I have marked `API Key` and `API Secret`. You can copy and paste them into [configuration form in instalation process](#filling-in-configuration-form-on-heroku) or set it when your app had been already deployed. (see [this instructions](#atrigger_key-and-atrigger_secret-setting))
5. [Verify atrigger with ATriggerVerify.txt](#atriggerverify.txt)
6. Now you can go back to [configuration instructions](#configuration).
###### `ATRIGGER_KEY` and `ATRIGGER_SECRET` setting
1. In order to find out how to get them, go [here](#atrigger.com-configuration)
2. If you already had them, time for [logging in to your website](#logging-in-to-your-website)
4. Now you should see a page like below. Now you can paste your `ATRIGGER_KEY` in right field and click `CHANGE` button.
![]
5. You should see a green confirmation like below
![]
6. Now you can paste your `ATRIGGER_SECRET` in right field and click `CHANGE` button. You should see similar green message. (example picture below)
![]
7. Now your `ATRIGGER_KEY` and `ATRIGGER_SECRET` are set. Go back to [atrigger configuration](atrigger.com-configuration).

#### ATriggerVerify.txt
1. Go to [atrigger setup website](https://atrigger.com/panel/setup) and download verification file. (picture below)
![]
2. Now [log in to your website](#logging-in-to-your-website)
3. You should see page like below. Click gray `Upload verification file` button.
![]
4. Click `Choose file` button and choose your ATriggerVerify.txt from your computer. (picture below)
![]
5. Click `UPLOAD` button. (picture below)
6. You should see green sucess message like below.
![]

# Logging in to your website
1. Go to your website (https://`<app_name>`.herokuapp.com). You should see page like below. Now click `IT IS MYWEBSITE >>` buttton.
  ![]
2. Now type your `SECRET_KEY` (it has been set during [instalation process](#filling-in-configuration-form-on-heroku)) and click `LOG IN` button. (example picture below)
![]
3. You are logged in !


# Notifications
**BetterMemorySugarBot** has two ways of notifying. I recomend notifying via **IFTTT**. It`s completly free, easier to set up and it is flexible. You can choose notifying via **facebook messenger**, **push notifications** from mobile app or **email**. Of course, you can explore this platform and combine BetterMemorySugarBot with other services on your own.Second options is **SMS via Twilio API**. I have to warn you, that **when free credits are run out, you will have to pay for text messages**. To use your free credits you do not have to give them any credit card or any other billing info. It is also a little more complicated to configurate than IFTTT. If you had decided, you can go to [notifications configuration instruction](#notifications-configuration-instructions)

#### Notifications configuration instruction
1. [Log in to your website](#logging-in-to-your-website)
2. Click blue `NOTIFICATIONS CENTER` button. (picture below)
![]
3.  Choose your notifications way (you can choose both) and click `CHANGE` button. (picture below)
![]
4. Now go to [IFTTT configuration](#ifttt-configuration) or to [SMS configuration](#sms-configuration)


#### IFTTT configurating
1. If you are here, I assume you had already followed [notifications configuration instruction](#notifications-configuration-instructions)
2. Create account on IFTTT or if you already done this, you can [log in](https://ifttt.com/login?wp_=1)
   * Go to [this link](https://ifttt.com)
   * You can sign up with your social media account or just type your email and click `Get started` button.
   * If you had choose email registration, now type your password and click `Sign up` button.
3. Now go to [this link](https://ifttt.com/services/maker_webhooks)
4. Click `Connect` button (picture below)
![]
5. Click `Documentation` button (picture below)
![]
6. Copy your key. (picture below)
![]
7. Now [log in to your website](#logging-in-to-your-website) and go to notifications center. You should see page like below.
![]
8. Click `MANAGE IFTTT MAKERS` button
9. Now paste your `IFTTT key` and click `ADD` button. (picture below)
10. Now you should see green message. (picture below)
![]
11. Of course, you can add more IFTTT accounts and BetterMemorySugarBot will trigger all of them.
12. Finally, time for creating your own notifying applet:
    * [Facebook Messenger notifications](#facebook-messenger)
    * [push notifications](#push-notifications) from IFTTT mobile app
    * [email](#email-notifications)
    * explore IFTTT and create some other custom applet
#### IFTTT Applets tutorials
#### Facebook Messenger
1. Go to [this link](https://ifttt.com/create)
2. Click `+this` button. (picture below)
![]
3. Search for `webhooks` and click it. (picture below)
![]
4. Click `Receive web request` (picture below)
![]
5. Type `sugarbot-notification` and click `Create trigger` button. (picture below)
![]
6. Click `+that` button. (picture below)
![]
7. Search for
     >messenger

    and click `Facebook Messenger` button. (picture below)
![]
8. Click `connect` button. (picture below)
![]
9. Log in to your Facebook account
![]
10. Click `Get Started` button. (picture below)
![]
11. You should see something like below
![]
12. Confirm your connection via link in your email box.(example picture below)
![]
13. Now get back to your applet creation site.
14. Click `Send message` button.  (picture below)
    * if do not see the same, just click `back` and repeat 7th step from this instruction
![]
15. In `Message text` field paste:
    >{{Value1}}
16. Click `Create action` button. (picture below)
![]
17. Click `Finish` button and now your applet is ready.
18. If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, you are ready to [turn this app on](#turn-it-on) !!!

#### Push Notifications
1. Go to [this link](https://ifttt.com/create)
2. Click `+this` button. (picture below)
![]
3. Search for `webhooks` and click it. (picture below)
![]
4. Click `Receive web request` (picture below)
![]
5. Type
   >sugarbot-notification

6. click `Create trigger` button. (picture below)
![]
6. Click `+that` button. (picture below)
![]
7. Search for
     >notifications

   and click `Notifications` button. (picture below)
![]
8. Click `connect` button. (picture below)
![]
14. Click `Send notifications from the IFTTT app` button.  (picture below)
![]
15. In `Message` field paste:
    >{{Value1}}
16. Click `Create action` button. (picture below)
![]
17. Click `Finish` button and now your applet is ready.
18. Now you just have to download IFTTT app and log in to your account. IFTTT asks you for your number. You can give it them and they will send you a link or just download it from [Google Play](http://ift.tt/google-play-download) or [App Store](http://ift.tt/app-store-download)
18. If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, you are ready to [turn this app on](#turn-it-on) !!!

#### Email notifications
1. Go to [this link](https://ifttt.com/create)
2. Click `+this` button. (picture below)
![]
3. Search for `webhooks` and click it. (picture below)
![]
4. Click `Receive web request` (picture below)
![]
5. Type
   >sugarbot-notification

6. click `Create trigger` button. (picture below)
![]
6. Click `+that` button. (picture below)
![]
7. Search for
     >email

   and click `email` button. (picture below)
![]
8. Click `connect` button. (picture below)
![]
9. Type your email and click `Send PIN` button.  (picture below)
![]
10. Go to your email box and copy your PIN. Paste it in `PIN` field. (picture below)
 ![]
11. Click `Connect` button.
12. Now get back to your applet creation site.
14. Click `Send me an email` button.  (picture below)
![]
14. In `Subject` field, type your custom message subject e.g. *"BetterMemorySugarBot Notification"*
15. In `Body` field paste:
    >{{Value1}}
16. Click `Create action` button. (picture below)
![]
17. Click `Finish` button and now your applet is ready.
18. If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, you are ready to [turn this app on](#turn-it-on) !!!

#### SMS configurating
This tutorial will be avaible soon.

# Turn it on
If you had done all the steps from [instalation](#instalation) and [configuration](#configuration) instructions, your app is fully prepared for this final step.
1. [Log in to your website](#logging-in-to-your-website)
2. Click `SEND NOTIFICATION NOW` green button. (picture below)
![]
3. You should see page similar to below one
![]
4. **Congratulations !!!** Your app is working. Your first notifications has been sended ! Now every day at give time, BetterMemorySugarBot will send you a notification with remaing time. If you wants to check remaing time without notification, just click `QUIET CHECKUP` button in menu.