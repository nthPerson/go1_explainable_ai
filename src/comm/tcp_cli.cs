using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using System;
using System.Net;
using System.Net.Sockets;

public class Client : MonoBehaviour
{  
    NavigationScript nav_data;
    private int port = 7000;
    private TcpClient client;

    private struct VectorStream
    {
        public float x;
        public float z;
    }

    void Start()
    {
        client = new TcpClient("localhost", port);
        nav_data = GetComponent<NavigationScript>();
    }

    void Update()
    {
        VectorStream message = new VectorStream();
        message.x = nav_data.velocity.x;
        message.z = nav_data.velocity.z;
        SendVectorStream(message);
    }

    Byte[] ConvertMessageToBytes(in VectorStream message)
    {
        Byte[] data_x = BitConverter.GetBytes(message.x);
        Byte[] data_z = BitConverter.GetBytes(message.z); 
        Byte[] data = new Byte[data_x.Length + data_z.Length];   
        System.Buffer.BlockCopy(data_x, 0, data, 0, data_x.Length);
        System.Buffer.BlockCopy(data_z, 0, data, data_x.Length, data_z.Length);
        return data;
    }

    void SendVectorStream(in VectorStream message)
    {
        try
        {            
            Byte[] byte_data = ConvertMessageToBytes(message);
            NetworkStream stream = client.GetStream();
            stream.Write(byte_data, 0, byte_data.Length);
            Debug.Log("VectorStream sent: " + message);
        }
        catch (Exception e)
        {
            Debug.Log("Error sending message: " + e);
        }
    }
}
