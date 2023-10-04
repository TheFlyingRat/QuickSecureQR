# QuickSecureQR
Generate a quick secure QR code with ease with Tkinter
V: Indev 0.1

[//]: # (add gui images here)

## Whats and Whys

### What's it for?
Originally, I ran into a very niche error where I couldn't get my absurdly long passwords into my phone from KeePassXC.

Since I couldn't be bothered typing in a 128 character purely random password directly from my open KeePassXC database on my PC screen into my phone, I'd use an online QR code generator to do this and then scan it on my phone to copy my password over.

Since I don't know how these QR code generators work, I was kind of skeptical, especially since some you have to click a submit button and it takes a while hence its not being rendered clientside and instead serverside.

Who knows who owns those servers!!!

That's where QuickSecureQR comes in. Generate a QUICK, and pretty SECURE QR code as a python script or executable application with `Tkinter` and `qrcode`

### Why is it quick?
Firstly, opening the program auto-highlights the password input field, so its ready off the bat.

It auto updates the QR code preview every time you release a key press on your computer, or just `ctrl+c` `ctrl+v` your password into the text field, so there's no interaction needed

Lastly, theres key binds, to both clear, hide and quit so you can use the keyboard the whole time while using it, maximizing your efficiency

### Why is it secure?
By default, both the password and QR code is hidden, so, while you type your password, or in case someones watching your screen, nothing can be read.

Once you've finished typing, or copying your password in, you can click the unhide checkbox for a 5-second visible time.

After the 5 seconds is up, both password and QR code is hidden again

Additional security will be implemented soon, see below

---
## Q&A

### But theres KeePass apps for mobile devices!
I know, however my KeePassXC database exists on my NAS, and this requires constant syncing and maintainance to prevent sync conflicts. Since iOS disallows file syncing in the background, this is a pain.

### There's websites that generate QR code clientside, why would you bother making this?
I don't always have an internet connection. It's either this, or a web app in JavaScript that I can run locally.

### Additional security? Like what?
Obviously the QR code needs to be generated somewhere, which is temporarily stored in the computers memory.

I need to add some sort of garbage collection that disposes of old QR previews before generating a new one on the fly. At least I think so, it might happen automatically? [TBC]

