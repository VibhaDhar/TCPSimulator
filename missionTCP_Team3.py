import heapq
import sys
import multiprocessing, tempfile
import socket
import threading
import socket,threading
from collections import OrderedDict
import SocketServer
import time
from struct import *
import struct
import logging
HOST='127.0.0.1'

import logging



class Graph:
    
    def __init__(self):
        self.vertices = {}
      
        
    def add_vertex(self, name, edges):
        self.vertices[name] = edges
        
                              
    
    def shortest_path(self, start, finish):
        distances = {} # Distance from start to node
        previous = {}  # Previous node in optimal path from source
        nodes = [] # Priority queue of all nodes in Graph

        for vertex in self.vertices:
            
            if vertex == start: # Set root node as distance of 0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None
        
        
        while nodes:
            smallest = heapq.heappop(nodes)[1] # Vertex in nodes with smallest distance in distances
            if smallest == finish: # If the closest node is our target we're done so print the path
                path = []
                while previous[smallest]: # Traverse through nodes til we reach the root which is 0
                    path.append(smallest)
                    smallest = previous[smallest]
                return path
            if distances[smallest] == sys.maxsize: # All remaining vertices are inaccessible from source
                break
            
            for neighbor in self.vertices[smallest]: # Look at all the nodes that this vertex is attached to
                alt = distances[smallest] + self.vertices[smallest][neighbor] # Alternative path distance
                if alt < distances[neighbor]: # If there is a new shortest path update our priority queue (relax)
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)
                
        return distances


    def __str__(self):
        return str(self.vertices)
            

def HandShake(src, dst, seq , aSeq, doff,fin , syn, rst, psh, ack, urg, chk, uptr):
        '''
        Wrap the TCP 3-way handshake procedure
        '''
        source_ip = '192.168.1.101'
        dest_ip = '192.168.1.1' # or socket.gethostbyname('www.google.com')
        
       
        tcp_source = src   # source port
        tcp_dest = dst   # destination port
        tcp_seq = 0
        tcp_ack_seq = tcp_seq + 1
        tcp_ack=1
        tcp_doff = doff  #4 bit field, size of tcp header, 5 * 4 = 20 bytes
        #tcp flags
        tcp_fin = fin
        tcp_syn = 1
        tcp_rst = rst
        tcp_psh = psh
        #tcp_ack = ack
        tcp_urg = urg
        tcp_window = socket.htons (5840)    #   maximum allowed window size
        tcp_check = chk
        tcp_urg_ptr = uptr
         
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
        print ("Inside" ) 
        # the ! in the pack format string means network order
        #tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
        tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
 
        user_data = ''
        
        # pseudo header fields
        source_address = socket.inet_aton( source_ip )
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(user_data)
         
        psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
        psh = psh + tcp_header + str(user_data);
         
        tcp_check = checksum(psh)
        
         
        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        
        tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
         
        packet =  tcp_header + user_data      
        if packet is None:
                raise RuntimeError('TCP handshake failed, connection timeout')
        
        if not (tcp_ack and tcp_syn):
            raise RuntimeError('TCP handshake failed, bad server response')
       
        
        return packet
        
           

def Packet_Create_Structure(filename,src, dst, seq , aSeq, doff,fin , syn, rst, psh, ack, urg, chk, uptr  ):
 packet = '';
 #filename='E:\Project1-5344\Transcripts(1)\Ann\Ann-_Chan.txt'
 with open (filename,'rb') as f:
         
   for packet in range(0,65555):
        
        #packet=f.read()
        source_ip = '192.168.1.101'
        dest_ip = '192.168.1.1' # or socket.gethostbyname('www.google.com')
        
       
        tcp_source = src   # source port
        tcp_dest = dst   # destination port
        tcp_seq = seq+1
        tcp_ack_seq = seq+2
        tcp_doff = doff   #4 bit field, size of tcp header, 5 * 4 = 20 bytes
        #tcp flags
        tcp_fin = fin
        tcp_syn = syn
        tcp_rst = rst
        tcp_psh = psh
        tcp_ack = ack
        tcp_urg = urg
        tcp_window = socket.htons (5840)    #   maximum allowed window size
        tcp_check = chk
        tcp_urg_ptr = uptr
         
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
        print ("Inside" ) 
        # the ! in the pack format string means network order
        tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
         
        user_data = f.read(15000)
        
        # pseudo header fields
        source_address = socket.inet_aton( source_ip )
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(user_data)
         
        psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
        psh = psh + tcp_header + str(user_data);
         
        tcp_check = checksum(psh)
        #print tcp_checksum
         
        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)
         
        # final full packet - syn packets dont have any data
        
        packet =  tcp_header + user_data
        offset=len(user_data)
        f.seek(offset)
       
        return packet
def checksum(msg):
    s = 0
     
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 16):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
        s = s + w
     
    s = (s>>16) + (s & 0xffff);
    s = s + (s >> 16);
     
    #complement and mask to 4 byte short
    s = ~s & 0xffff
     
    return s    
global seq #---------------------------------------------------Global Sequence number to keep track of messages
seq=0
def RandomPacketGeneration(src, dst, urg , rst, ter):
        source_ip = '192.168.1.101'
        dest_ip = '192.168.1.1' # or socket.gethostbyname('www.google.com')
        global seq
     
        tcp_source = src   # source port
        tcp_dest = dst   # destination port
       
        
        tcp_seq = seq
        print tcp_seq
        tcp_ack_seq = tcp_seq + 1
        
        print tcp_ack_seq
        tcp_doff = 5   #4 bit field, size of tcp header, 5 * 4 = 20 bytes
        #tcp flags
        tcp_fin = 0
        tcp_syn = 0
        tcp_rst = rst
        tcp_ter = ter
        tcp_ack = 0
        tcp_urg = urg
        tcp_window = socket.htons (5840)    #   maximum allowed window size
        tcp_check = 0
        tcp_urg_ptr = 0
         
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_ter <<3) + (tcp_ack << 4) + (tcp_urg << 5)
        print ("Inside" ) 
        # the ! in the pack format string means network order
        tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
         
        user_data = ''
        
        # pseudo header fields
        source_address = socket.inet_aton( source_ip )
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(user_data)
         
        psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
        psh = psh + tcp_header + str(user_data);
         
        tcp_check = checksum(psh)
        #print tcp_checksum
         
        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)
         
        # final full packet - syn packets dont have any data
        
        packet =  tcp_header + user_data
        #offset=len(user_data)
        #f.seek(offset)
        

        seq=seq+1
        return packet
        

def extractSeqAck():
    
    sentPacket=Tcp_Segment_Structure(8000, 9000, 0 , 0, 5,0 , 1, 0, 0, 0, 0,0, 0 )
    rcvdPacket=Tcp_Segment_Structure(8000, 9000, 1 , 1, 5,0 , 1, 0, 0, 0, 0,0, 0 )
    sentHeader=struct.unpack("!HHLLBBHHH",sentPacket[0:20])
    rcvdHeader=struct.unpack("!HHLLBBHHH",rcvdPacket[0:20])
    
   

    
    seqNo= sentHeader[2]
    ackNo= sentHeader[3]

    seqNo1=rcvdHeader[2]
    ackNo1=rcvdHeader[3]

    dataLength= len(sentPacket)-20
    dataLength1= len(rcvdPacket)-20
    
    print ("seqNo Sent", seqNo)
    print ("Ack Sent", ackNo)
    
    print ("seqNo Recieved", seqNo1)
    print ("Ack Recieved", ackNo1)
    

    newSeq=ackNo1
    newAck=seqNo1+dataLength1
    print (newSeq)
    print (newAck)


    

def SetFlags():
    Flags=str(raw_input('Which flag you want to set ?'))
    if Flags=='URG':
        Tcp_Segment_Structure(8000, 9000, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
    elif Flags=='TER':
        Tcp_Segment_Structure(8000, 9000, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
        exit()
        
def WriteLog():
    link1 = open('abc1', 'ab+')
    link2= open('abc2', 'ab+')
    link3 = open('abc3', 'ab+')
    link102=open('abc4', 'ab+')
    link107=open('abc5', 'ab+')
    link104=open('abc6', 'ab+')
    link105=open('abc7', 'ab+')
    link106=open('abc8', 'ab+')
    link1021=open('abc8', 'ab+')




Ann = multiprocessing.Queue()
Chan = multiprocessing.Queue()
Jan =multiprocessing.Queue()
A=multiprocessing.Queue()
B=multiprocessing.Queue()
C = multiprocessing.Queue()
D=multiprocessing.Queue()
E=multiprocessing.Queue()
F = multiprocessing.Queue()
G=multiprocessing.Queue()
H=multiprocessing.Queue()
L=multiprocessing.Queue()


       

    


        
        
if __name__ == '__main__':


        logging.basicConfig(filename='E:/Log1', filemode='a',format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level='DEBUG')
   #--------------------Router------------#
        g = Graph()


        g.add_vertex('A', {'B': 4, 'C': 3, 'E': 7, 'Ann': 0})
        g.add_vertex('B', {'A': 4, 'C': 6, 'L': 5})
        g.add_vertex('C', {'A': 3, 'B': 6, 'D': 11})
        g.add_vertex('D', {'C': 11, 'F':6, 'G': 10, 'L': 9})
        g.add_vertex('E', {'A': 7,  'G': 5, 'Chan':0})
        g.add_vertex('F', {'L': 5, 'D': 6, 'Jan': 0})
        g.add_vertex('G', {'D': 10, 'E': 5})
        g.add_vertex('H', {'F': 0})
        g.add_vertex('L', {'B': 5,'D': 9, 'F':5})
        g.add_vertex('Ann', {'A': 0})
        g.add_vertex('Chan', {'E': 0})
        g.add_vertex('Jan', {'H': 0, 'F':0})


        #print(g.shortest_path('Chan', 'Ann'))
        route1=g.shortest_path('Chan', 'Ann')
        route1.append('Chan')
        route3=g.shortest_path('Chan','Jan')
        route3.append('Chan')
                               
        route2=g.shortest_path('Ann','Jan')
        route2.append('Ann')
        route4=g.shortest_path('Ann','Chan')
        route4.append('Ann')

        route5=g.shortest_path('Jan','Chan')
        route5.append('Jan')
        route6=g.shortest_path('Jan','Ann')
        route6.append('Jan')
        print ('Dijsktra')#-----------------------------------Dijkstra-------------------------
        print (route1)
        print (route2)
        print (route3)
        print (route4)
        print (route5)
        print (route6)
        import logging
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # first file logger
        logger_1 = logging.getLogger('simple_logger')
        hdlr_1 = logging.FileHandler('E:/simplefile_1.log')
        hdlr_1.setFormatter(formatter)
        logger_1.addHandler(hdlr_1)

        # second file logger
        logger_2 = logging.getLogger('simple_logger_2')
        hdlr_2 = logging.FileHandler('E:/simplefile_2.log')    
        hdlr_2.setFormatter(formatter)
        logger_2.addHandler(hdlr_2)


        # third file logger
        logger_3 = logging.getLogger('simple_logger_3')
        hdlr_3 = logging.FileHandler('E:/simplefile_3.log')    
        hdlr_3.setFormatter(formatter)
        logger_3.addHandler(hdlr_3)


        #fourth file logger 
        logger_4 = logging.getLogger('simple_logger_4')
        hdlr_4 = logging.FileHandler('E:/simplefile_4.log')
        hdlr_4.setFormatter(formatter)
        logger_4.addHandler(hdlr_4)

        # ifth file logger
        logger_5 = logging.getLogger('simple_logger_5')
        hdlr_5 = logging.FileHandler('E:/simplefile_5.log')    
        hdlr_5.setFormatter(formatter)
        logger_5.addHandler(hdlr_5)


        # third file logger
        logger_6 = logging.getLogger('simple_logger_6')
        hdlr_6 = logging.FileHandler('E:/simplefile_6.log')    
        hdlr_6.setFormatter(formatter)
        logger_6.addHandler(hdlr_6)



        

        #--------AnnToChan----------------------------------------------------------#
        AnnToChanH=HandShake(111, 001, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
        #HandShake(src, dst, seq , aSeq, doff,fin , syn, rst, psh, ack, urg, chk, uptr)
        #Chan replies back to the Handshake
        RecvdPacket1=struct.unpack("!HHLLBBHHH",AnnToChanH[0:20])
        seqNo= RecvdPacket1[2]
        logger_1.info('AnnToChan')
        ackNo= RecvdPacket1[3]
        tcp_syn=RecvdPacket1[6]
        if(ackNo==1 ):
            print ("Handshake successfull between Ann and Chan")
            logger_1.info('Handshake successfull between Ann and Chan')
            AnnToChan=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Ann\Ann-_Chan.txt',111, 001, 1 , 1, 5,0 , 1, 0, 0, 0, 0,0, 0 )
            Ann.put(AnnToChan)
            
            a=Ann.get()
            A.put(a)
            logger_1.info('Sending data from Ann to A')
            a=A.get()
            E.put(a)
            a=E.get()
            logger_1.info('Sending data from A to E')
            Chan.put(a)
            a=Chan.get()
            print (a)
            logger_1.info('Sending data from E to Chan')
           #----Reliability---------------------------------------------------------#           
        for i in range(0,5):
                randomPacket=RandomPacketGeneration(111,001, 0, 0, 0)
                if i == 4:
                       #randomPacket=RandomPacketGeneration(111,001, 0, 1, 0)
                        logger_1.info('Flooding Packets for Reliability check and dropping after the 5th packet')
                        break

        randomPacket=RandomPacketGeneration(111,001,0,0,0)
        #-----------Over from Ann To Chan---------------------------------------------#







        #-----------------Jan To Ann-------------------------------------------------#
        JantoAnnH=HandShake(100, 111, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0)
        #HandShake(src, dst, seq , aSeq, doff,fin , syn, rst, psh, ack, urg, chk, uptr)
        #Chan replies back to the Handshake
        RecvdPacket2=struct.unpack("!HHLLBBHHH",JantoAnnH[0:20])
        seqNo2= RecvdPacket2[2]
        ackNo2= RecvdPacket2[3]
        tcp_syn2=RecvdPacket2[6]
        logger_2.info("Jan To Ann-")
        if(ackNo2==1 ):
            print ("Handshake successfull between Jan and Ann")
            logger_2.info("Jan To F-")
            JantoAnn=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Jan\Jan-_Ann.txt',100, 111, 0 , 0, 5,0 , 1, 0, 0, 0, 0,0, 0 )
            Jan.put(JantoAnn)
            b=Jan.get()
            #print (b)
            F.put(b)
        
            b=F.get()
            L.put(b)
            logger_2.info("F To L")
            b=L.get()
            B.put(b)
            b=B.get()
            logger_2.info("L To B")
            A.put(b)
            b=A.get()
            logger_2.info("B to A")
            Ann.put(b)
            b=Ann.get()
            logger_2.info("A to Ann")
            print (b)



        #------------Jan To Chan---------------------------------------------------------#

        JantoChanH=HandShake(100, 111, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0)
        RecvdPacket3=struct.unpack("!HHLLBBHHH",JantoAnnH[0:20])
        seqNo3= RecvdPacket3[2]
        ackNo3= RecvdPacket3[3]
        tcp_syn3=RecvdPacket3[6]
        logger_3.info("Jan to Chan")
        if(ackNo3==1 ):
            print ("Handshake successfull between Jan and Chan")
            logger_3.info("Handshake successfull between Jan and Chan")
            logger_3.info("Jan To Chan")
            JantoChanH=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Jan\Jan-_Chan.txt',111, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 0,0, 0 )
            Jan.put(JantoChanH)
            c=Jan.get()
            #print (c)
            F.put(c)
            logger_3.info("Jan To F")
            c=F.get()
            D.put(c)
            logger_3.info("F To D")
            c=D.get()
            G.put(c)
            logger_3.info("D To G")
            c=G.get()
            E.put(c)
            c=E.get()
            logger_3.info("G To E")
            Chan.put(c)
            c=Chan.get()
            logger_3.info("E To Chan")
            print (c)
        #---------------------------Chan To Ann-------------------------------------------#

        ChantoAnnH=HandShake(001, 111, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0)
        RecvdPacket4=struct.unpack("!HHLLBBHHH",ChantoAnnH[0:20])
        seqNo4= RecvdPacket4[2]
        ackNo4= RecvdPacket4[3]
        tcp_syn4=RecvdPacket3[6]
        logger_4.info("Chan to Ann Communication")
        if(ackNo4==1 ):
            print ("Handshake successfull between Chan and Ann")
            logger_4.info("Handshake successfull between Chan and Ann")
            ChantoAnn=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Chan\Chan-_Ann.txt',001, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 0,0, 0 )
            Chan.put(ChantoAnn)
            d=Chan.get()
            logger_4.info("Chan to E")
            #print (c)
            E.put(d)
            logger_4.info("E to A")
            d=E.get()
            A.put(d)
            logger_4.info("A to Ann")
            d=A.get()
            Ann.put(d)
            logger_4.info(" Ann reeived")
            print (d)


        #--------------------Chan to Jan---------------------------------------------------#

        ChantoJanH=HandShake(001, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0)
        RecvdPacket5=struct.unpack("!HHLLBBHHH",ChantoJanH[0:20])
        seqNo5= RecvdPacket5[2]
        ackNo5= RecvdPacket5[3]
        tcp_syn5=RecvdPacket3[6]
        logger_5.info("Chan to Jan Communication")
        if(ackNo5==1 ):
            print ("Handshake successfull between Chan to Jan")
            #ChantoAnn=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Chan\Chan-_Ann.txt',001, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
            ChanToJan=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Chan\Chan-_Jan.txt',001, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 0,0, 0 )
            Chan.put(ChanToJan)
            e=Chan.get()
            #print (c)
            E.put(e)
            logger_5.info("Chan to E")
            e=E.get()
            A.put(e)
            logger_5.info("E to A")
            e=A.get()
            B.put(e)
            logger_5.info("A to B")
            e=B.get()
            L.put(e)
            logger_5.info("B to L")
            e=L.get()
            F.put(e)
            logger_5.info("L to F")
            e=F.get()
            Jan.put(e)
            logger_5.info("F to Jan")
            
            print (e)

        #---------------Ann to Jan-------------------------------------------------#
            
        AnntoJanH=HandShake(111, 001, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
        RecvdPacket6=struct.unpack("!HHLLBBHHH",AnntoJanH[0:20])
        seqNo6= RecvdPacket6[2]
        ackNo6= RecvdPacket6[3]
        tcp_syn6=RecvdPacket6[6]
        logger_6.info("Ann to Jan Communication")
        if(ackNo6==1 ):
            print ("Handshake successfull between Jan and Ann")
            #ChantoAnn=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Chan\Chan-_Ann.txt',001, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
            #ChanToJan=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Chan\Chan-_Jan.txt',001, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
            AnntoJan=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Ann\Ann-_Jan.txt',111, 100, 0 , 0, 5,0 , 1, 0, 0, 0, 1,0, 0 )
            Ann.put(AnntoJan)
            f=Ann.get()
            #print (c)
            logger_6.info("Ann to A")
            A.put(f)
            f=A.get()
            logger_6.info("A to B")
            B.put(f)
            f=B.get()
            logger_6.info("B to L")
            L.put(f)
            f=L.get()
            logger_6.info("L to F")
            F.put(f)
            f=F.get()
            logger_6.info("F to Jan")
            Jan.put(f)
            logger_6.info("Jan Received")
            Chan.close()#-------------------------Closing connection with Chan after Communication between Ann to Jan and Ann downloads the file------
            Flags=str(raw_input('Which flag you want to set ?'))
            if Flags=='TER':#----------------------------------------Setting the TER flag and terminate-----------------
                AnnToChan=Packet_Create_Structure('E:\Project1-5344\Transcripts(1)\Ann\Ann-_Chan.txt',111, 001, 1 , 1, 5,0 , 1, 0, 1, 0, 0,0, 0 )
                exit()
            filename='E:/simplefile_1.log'
            with open (filename,'r') as f:
                a=f.read()
            logger_6.info("Communiction with Chan")
            link1 = open('E:/simplefile_6', 'ab+')
            link1.write(a)
            
            print (f)
       
      
