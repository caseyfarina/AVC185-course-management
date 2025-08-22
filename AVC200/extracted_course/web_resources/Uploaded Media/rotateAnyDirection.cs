using UnityEngine;
using System.Collections;

public class rotateAnyDirection : MonoBehaviour
{
    public Vector3 rotationSpeed = new Vector3(0,50,0);
    // Before rendering each frame..
    void Update()
    {
        // Rotate the game object that this script is attached to by 15 in the X axis,
        // 30 in the Y axis and 45 in the Z axis, multiplied by deltaTime in order to make it per second
        // rather than per frame.
        transform.Rotate(rotationSpeed * Time.deltaTime);
       
    }
}
