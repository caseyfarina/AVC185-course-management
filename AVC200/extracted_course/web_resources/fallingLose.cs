using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class fallingLose : MonoBehaviour
{
   
    public GameObject LoseMessage;
    public float fallThreshold = -10f;
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(transform.position.y <= fallThreshold)
        {
            LoseMessage.SetActive(true);
        }
    }
}
