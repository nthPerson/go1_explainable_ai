using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class Server : MonoBehaviour
{
    private const int port = 7000;
    private TcpListener tcpListener;
    private TcpClient connectedClient;
    private NetworkStream networkStream;

    void Start()
    {
        StartListening();
    }

    void StartListening()
    {
        try
        {
            tcpListener = new TcpListener(IPAddress.Any, port);
            tcpListener.Start();
            Debug.Log("Server started on port " + port);
            StartCoroutine(AcceptClients());
        }
        catch (Exception e)
        {
            Debug.LogError("Error starting server: " + e.Message);
        }
    }

    private IEnumerator AcceptClients()
    {
        while (true)
        {
            if (tcpListener.Pending())
            {
                connectedClient = tcpListener.AcceptTcpClient();
                networkStream = connectedClient.GetStream();
                StartCoroutine(HandleClient(connectedClient, networkStream));
            }
            yield return null;  
        }
    }

    private IEnumerator HandleClient(TcpClient client, NetworkStream stream)
    {
        byte[] buffer = new byte[1024];
        try
        {
            while (client.Connected)
            {
                if (stream.DataAvailable)
                {
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string receivedText = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                        Debug.Log("Received data: " + receivedText);
                    }
                }
                yield return null;  
            }
        }
        catch (Exception e)
        {
            Debug.LogError("Error handling client: " + e.Message);
        }
        finally
        {
            stream.Close();
            client.Close();
        }
    }

    void OnDestroy()
    {
        if (networkStream != null)
            networkStream.Close();
        if (connectedClient != null)
            connectedClient.Close();
        if (tcpListener != null)
        {
            tcpListener.Stop();
            Debug.Log("Server stopped.");
        }
    }
}
