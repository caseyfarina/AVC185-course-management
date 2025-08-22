using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class resetRootMotion : MonoBehaviour
{

    public float resetPosition = -6f;
    private Vector3 original_Position;

    public enum directions { Left, Right, Up, Down};
    public directions current_direction;
    
    
    // Start is called before the first frame update
    void Start()
    {
        original_Position = transform.position;
    }

    // Update is called once per frame
    void Update()
    {

        if (current_direction == directions.Left)
        {
            if (transform.position.x < resetPosition)
            {
                transform.position = new Vector3(original_Position.x, original_Position.y, original_Position.z);
            }
        }
        if (current_direction == directions.Right)
        {
            if (transform.position.x > resetPosition)
            {
                transform.position = new Vector3(original_Position.x, original_Position.y, original_Position.z);
            }
        }
        if (current_direction == directions.Up)
        {
            if (transform.position.y > resetPosition)
            {
                transform.position = new Vector3(original_Position.x, original_Position.y, original_Position.z);
            }
        }
        if (current_direction == directions.Down)
        {
            if (transform.position.y < resetPosition)
            {
                transform.position = new Vector3(original_Position.x, original_Position.y, original_Position.z);
            }
        }
    }
}
