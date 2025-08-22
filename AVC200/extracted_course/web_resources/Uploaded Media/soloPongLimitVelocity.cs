using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class soloPongLimitVelocity : MonoBehaviour
{
    Rigidbody2D thisBody;
    public float maxVelocity = 500f;
    public float smoothFactor = .99f;

    // Start is called before the first frame update
    void Start()
    {
        thisBody = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void FixedUpdate()
    {
        if (thisBody.velocity.sqrMagnitude > maxVelocity)
        {
            //smoothness of the slowdown is controlled by the 0.99f, 
            //0.5f is less smooth, 0.9999f is more smooth
            thisBody.velocity *= smoothFactor;
        }
    }
}
