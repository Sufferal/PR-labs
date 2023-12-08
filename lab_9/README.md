# Issue
FTP link is not working, because FTP has fallen out of use and is not supported by most browsers.

# Solution
Use HTTP link instead of FTP link.

# Code 
If you have control over the server or hosting configuration, you can try adding the following line to your server's configuration or .htaccess file:
```
AddType application/octet-stream .txt
```

Here's the link that includes a fallback for users who can't download directly:
```
<a href="https://montane-concepts.000webhostapp.com/downloads/goodbye.txt" download="goodbye.txt" target="_blank" rel="noopener noreferrer">Download text</a>
```