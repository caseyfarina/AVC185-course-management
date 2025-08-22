using UnityEngine;
using System.Collections;

public class attachBot : MonoBehaviour {

	// store a public reference to the Player game object, so we can refer to it's Transform
	public GameObject player;
    public float yOffset = .2f;

    private Rigidbody body;
	// Store a Vector3 offset from the player (a distance to place the camera from the player at all times)
	private Vector3 offset;

	// At the start of the game..
	void Start ()
	{
		// Create an offset by subtracting the Camera's position from the player's position
		offset = transform.position - player.transform.position;
        body = player.GetComponent<Rigidbody>();
	}

	// After the standard 'Update()' loop runs, and just before each frame is rendered..
	void LateUpdate ()
	{
		// Set the position of the Camera (the game object this script is attached to)
		// to the player's position, plus the offset amount
		transform.position = player.transform.position + offset;

        Vector3 displaceLook = new Vector3(body.velocity.x, body.velocity.y, body.velocity.z);
        //displaceLook = Vector3.SmoothDamp()
        // transform.LookAt(displaceLook);
        Quaternion flatlook = Quaternion.LookRotation(displaceLook,Vector3.up);
        //flatlook = new Quaternion()
        flatlook.x = 0f;
        flatlook.z = 0f;
       //flatlook.w = 0f;
        transform.rotation = flatlook;


        //transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.LookRotation(displaceLook), Time.time * 1f);
    }
}