using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class shipControl : MonoBehaviour
{
    //public variable to control the forward thrust
    public float forwardThrust = 200f;

    //public variable to control the backwars thrust
    public float backwardThrust = 102f;

    //public variable to control the torque power
    public float torqueThrust = 4f;

    // set aside space for the rigidbody and name it thisBody
    Rigidbody2D thisBody;

    // Start is called before the first frame update
    void Start()
    {
        //grab a reference to the current Rigidbody2D
        thisBody = GetComponent<Rigidbody2D>();

        
    }

    // Update is called once per frame
    void Update()
    {
        //push the ship forward if you press the up arrow
        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            //adds forward thrust to the ship
            thisBody.AddForce(transform.up * forwardThrust);
        }

        //push the ship backwards if you press the down arrow
        if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            //adds forward thrust to the ship
            thisBody.AddForce(-transform.up * backwardThrust);
        }

        //turn the ship righ if you press the down arrow
        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            //adds torque to the ship
            thisBody.AddTorque(-torqueThrust, ForceMode2D.Impulse);
        }

        //turn the ship left if you press the down arrow
        if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            //adds torque to the ship
            thisBody.AddTorque(torqueThrust, ForceMode2D.Impulse);
        }


    }
}
