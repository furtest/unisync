Unisync is a data synchronisation tool written in python and based on [unison](https://github.com/bcpierce00/unison).  
I couldn't find a tool to fulfill the requirements I had for a synchronisation tool so I am creating my own as a wrapper around unison.  

# Goal

Unisync purpose is to keep personal data synchronised between multiple machines without needing to have all the data present an all the machines at the same time. For example you might not need to have your movies on your laptop but still want them on your desktop at home or you might want to keep your old pictures only on a server.
Unisync requires you to have a "server" (like a NAS at home) that will store all your data allowing you to only copy what you need when you need it.  
The issue is that you need to know what data is stored on the server to avoid conflict if creating duplicate files or folders. To address this unisync places a symlink for every file you do not wish to keep locally and allows you to mount the remote filesystem (using sshfs) allowing you to access files that aren't synchronised.  

# Developement

Unisync was at first a simple bash script but as it grew more complex I started struggling to maintain it which is why I am porting it to python. It will make everything more robust, easier to maintain and to add functionalities.  
I am in the early stages of the developement process, this should be usable in the upcoming weeks.  
Help will be welcome in the future but is not desirable right now as I want to shape this the way I want to.
