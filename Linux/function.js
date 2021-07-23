
   if (type === "same-origin") 
     frame.src = echoURL(content);
    else if (type === "cross-site") 
     frame.src = `$get_host_info().HTTP_NOTSAMESITE_ORIGIN$echoURL(content)`;
    else 
     frame.srcdoc = content;
   
 