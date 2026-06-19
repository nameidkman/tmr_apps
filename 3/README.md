the main loop connects to the MyWidget() which is a class in qt which we use and then modify inorder to be able to use osme of the other more useful function like the resize and such





the main system is that we had to make a system where you are able to see two different feeds of camera like a live stream so what i ended up doing is that i had a single camera which was using the webcam attached to the laptop and for the second one ended up using the default video which was provided in the "hello\_world" gstreamer program. 



the main layout is a grid layout with two main feed label on both of the sides. After doing the basics layout you go into the gstreamer 



for the main camera pipleline you have to convert the video feed from the webcam into a r-raw so that you are able to do things like set the camera width, height and get the overall RGB for the system and then in the end the apsink give the overall frames which you have gotten from the gstreamer to python which is used in the overall thing. 





for the video piple line i ended up using https://gstreamer.freedesktop.org/data/media/sintel\_trailer-480p.webm as i know it would work and was a good valuable option. In which you first have to convert the video to color space then you have to scale the video accordingly and then do the same thing like in the camera where you give the overall frames to python where its handled by qt to make everything work. After the basics conversion you have to add the custom sink and then 



