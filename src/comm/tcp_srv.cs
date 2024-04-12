using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class BNO055 : MonoBehaviour
{
    private const int port = 12121;
    private const int bufferSize = 1024;
    private TcpListener tcpListener;
    private byte[] receiveBuffer = new byte[bufferSize];

    void Start()
    {
        StartListening();
    }

    void Update()
    {
        ReceiveData();
    }

    void StartListening()
    {
        try
        {
            tcpListener = new TcpListener(IPAddress.Any, port);
            tcpListener.Start();
            Debug.Log("Socket listener started on port " + port);
        }
        catch (Exception e)
        {
            Debug.LogError("Error starting socket listener: " + e.Message);
        }
    }

    void ReceiveData()
    {
        if (tcpListener == null)
        {
            return;
        }

        if (tcpListener.Pending())
        {
            TcpClient client = tcpListener.AcceptTcpClient();
            NetworkStream stream = client.GetStream();
            int bytesRead = stream.Read(receiveBuffer, 0, bufferSize);
            if (bytesRead > 0)
            {
                
            }
            client.Close();
            stream.Close();
        }
    }

    private void OnDestroy()
    {
        if (tcpListener != null)
        {
            tcpListener.Stop();
            Debug.Log("Socket listener stopped.");
        }
    }
}