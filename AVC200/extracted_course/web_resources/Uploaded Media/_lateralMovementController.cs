

using UnityEngine;

public class _lateralMovementController : MonoBehaviour
{
    [SerializeField]
    private float moveSpeed = 5.0f; // Movement speed
    [SerializeField]
    private float minX = -5.0f; // Minimum X position
    [SerializeField]
    private float maxX = 5.0f; // Maximum X position

    private void Update()
    {
        // Get the horizontal input (left or right arrow key or A/D keys)
        float horizontalInput = Input.GetAxis("Horizontal");

        // Calculate the new position
        Vector3 newPosition = transform.position + Vector3.right * horizontalInput * moveSpeed * Time.deltaTime;

        // Clamp the X position within the specified range
        newPosition.x = Mathf.Clamp(newPosition.x, minX, maxX);

        // Update the object's position
        transform.position = newPosition;
    }
}
