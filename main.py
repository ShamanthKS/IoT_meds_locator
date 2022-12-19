import network
import socket
import time
import machine
import rp2
  
from machine import Pin

#defining GPIO pins for LEDs
amoxi = Pin(0, Pin.OUT) 
ibupro = Pin(1, Pin.OUT)
cetri = Pin(2, Pin.OUT)
paraceta = Pin(3, Pin.OUT)
asp = Pin(4, Pin.OUT)
vitad = Pin(5, Pin.OUT)
board_led = machine.Pin('LED', machine.Pin.OUT)
board_led.off()

#WiFi SSID and password
ssid = 'Sks'            
password = '9008496543'

#Country name in 2 letters (India = IN)
rp2.country('IN')     

def connect():    #Function for connecting to Wi-Fi
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(2)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}') #Display IP address
    
#.html document with css and javascript
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"> 
    <title>ARS Medicals</title>

</head>
<style>
    h2 {text-align: center;}
    .card{
        transition: all 0.5s ease-in-out;
        cursor: pointer;
        box-shadow: 0px 0px 6px -4px rgba(0,0,0,0.75);
        border-radius: 10px;
    }
.card:hover{
    box-shadow: 0px 0px 51px -36px rgba(0,0,0,1);
}


</style>

<body>
    <h1 class="text-center mt-2">ARS MEDICALS<img src="https://i.postimg.cc/QtvbhDhD/hospital-plus-icon-medical-health-symbol-vector-illustration-662353-370.webp" alt="Med symbol" style="width:80px;height:80px;"></h1>
    <h5 class="text-center mt-2">Opp. Foodland Hotel, Nitte 574110</h5>

    <input type="text" class="form-control mt-3 mx-auto" id="myinput" placeholder="Search for medicines..." style="width:30%;">


<div class="container mb-5">
    <h3 class="text-danger mt-5 text-center" id="para" style="display: none;">Not Found </h3>
    
    <div class="row mt-3" id="card">

    </div>

</div>



<script>
let filterarray =[];

// gallery card array

let galleryarray = [
    {
        id:1,
        name : "paracetamol",
        src: "https://5.imimg.com/data5/SELLER/Default/2022/9/IV/UY/CG/75459511/500mg-paracetamol-tablet-500x500.jpg",
        href: "/paraceta_led/on",
        desc : " "
    },
    {
        id:2,
        name : "amoxicillin",
        src: "https://barakat-pharma.com/wp-content/uploads/2019/09/all_0056_Amoxicillin.jpg",
        href: "/amoxi_led/on",
        desc : " "
    },
    {
        id:3,
        name : "ibuprofen",
        src: "https://5.imimg.com/data5/FQ/PP/IS/SELLER-7034457/ibuprofen-tablets-1000x1000.jpg",
        href: "/ibupro_led/on",
        desc : " "
    },
    {
        id:4,
        name : "cetrizine hydrochloride",
        src: "https://cpimg.tistatic.com/06447851/b/4/Cetirizine-Hydrochloride-Tablets.jpg",
        href: "/cetri_led/on",
        desc : " "
    },
    {
        id:5,
        name : "aspirin",
        src: "https://emedz.net/blog/wp-content/uploads/2019/08/aspirin.jpeg",
        href: "/asp_led/on",
        desc : " "
    },
    {
        id:6,
        name : "vitamin d",
        src: "https://5.imimg.com/data5/WH/BF/RA/SELLER-106130794/33-d-rise-60-k-cap-mrp-129-47-up-to-15-discount--500x500.jpg",
        href: "/vitad_led/on",
        desc : " "
    }
   ];



showgallery(galleryarray);


// create function to show card


function showgallery(curarra){
   document.getElementById("card").innerText = "";
   for(var i=0;i<curarra.length;i++){
       document.getElementById("card").innerHTML += `
        <div class="col-md-4 mt-3" >
           <div class="card p-3 ps-5 pe-5">
               <h4 class="text-capitalize text-center">${curarra[i].name}</h4>

          <img src="${curarra[i].src}" width="100%" height="320px"/>
          <p class="mt-2">${curarra[i].desc}</p>
          <a href="${curarra[i].href}" class="btn btn-primary stretched-link w-100 mx-auto">Find</a>
       
          </div>
          </div>
       `
   }

}

// For Live Searching Product

document.getElementById("myinput").addEventListener("keyup",function(){
    let text = document.getElementById("myinput").value.toLowerCase(); 

    filterarray= galleryarray.filter(function(a){
        if(a.name.toLowerCase().includes(text.toLowerCase())){
            return a.name;
           }

   });
   if(this.value==""){
       showgallery(galleryarray);
   }
   else{
       if(filterarray == ""){
           document.getElementById("para").style.display = 'block'
           document.getElementById("card").innerHTML = ""; 
       }
       else{

           showgallery(filterarray);
           document.getElementById("para").style.display = 'none'
       }
   }

});
</script>
    
</body>
</html>
    
"""
try:          #Attempt to connect to Wi-Fi
    connect()
    
except KeyboardInterrupt:
    board_led.off()
    time.sleep(1)
    machine.reset()
    
 
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
 
s = socket.socket()
s.bind(addr)
s.listen(1)
time.sleep(2)
 
print('listening on', addr)
board_led.on()          #Turn on onboard LED once socket is opened
count = 0
 
# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)

        request = cl.recv(1024)
        print(request)         #Listening for 'GET' requests
        # Comparing GET requests. If a GET request is found, the 'request.find'
        # function stores the value after how many string values it is found
        # In this case, it is '6'. Otherwise, it will return '-1'
        request = str(request)
        amoxi_on = request.find('/amoxi_led/on')
        ibupro_on = request.find('/ibupro_led/on')
        cetri_on = request.find('/cetri_led/on')
        paraceta_on = request.find('/paraceta_led/on')
        asp_on = request.find('/asp_led/on')
        vitad_on = request.find('/vitad_led/on') 
        
        print( 'amoxi on = ' + str(amoxi_on))
        print( 'ibupro on= ' + str(ibupro_on))
        print( 'cetri on = ' + str(cetri_on))
        print( 'paraceta on = ' + str(paraceta_on))
        print( 'asp on = ' + str(asp_on))
        print( 'vitad on = ' + str(vitad_on))
        
        if count == 1: #This condition is implemented when LED is turned on
            count = 0
            time.sleep(5)
            amoxi.value(0)
            ibupro.value(0)
            cetri.value(0)
            paraceta.value(0)
            asp.value(0)
            vitad.value(0)
            print('Server is ready')
            

        if amoxi_on == 6:
            print("amoxi on")
            amoxi.value(1)
            count = count+1
            
        if ibupro_on == 6:
            print("ibupro on")
            ibupro.value(1)
            count = count+1
            
        if cetri_on == 6:
            print("cetri on")
            cetri.value(1)
            count = count+1
            
        if paraceta_on == 6:
            print("paraceta on")
            paraceta.value(1)
            count = count+1
            
        if asp_on == 6:
            print("asp on")
            asp.value(1)
            count = count+1
            
        if vitad_on == 6:
            print("vitad on")
            vitad.value(1)
            count = count+1
            
        print('Count = ' +str(count))
        
        response = html
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response) #Send response to the client
        cl.close()      #Close the connection
        
    except OSError as e:
        cl.close()
        print('connection closed')