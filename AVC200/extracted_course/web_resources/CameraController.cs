using UnityEngine;

public class CameraController : MonoBehaviour {

    public float panSpeed = 20f;
    public float panBorderThickness = 10f;
    public float panLimitX =  5f;
    public float panLimitY = 5f;

    public float ScrollSpeed = 20f;
    public float cameraZoomMin = -20f;
    public float cameraZoomMax = -40f;

	// Update is called once per frame
	void Update () {

        Vector3 pos = transform.position;

        if (Input.mousePosition.y >= Screen.height - panBorderThickness)
        {
            pos.y += panSpeed * Time.deltaTime;
        }
        if (Input.mousePosition.y <= panBorderThickness)
        {
            pos.y -= panSpeed * Time.deltaTime;
        }
        if (Input.mousePosition.x >= Screen.width - panBorderThickness)
        {
            pos.x += panSpeed * Time.deltaTime;
        }
        if (Input.mousePosition.x <= panBorderThickness)
        {
            pos.x -= panSpeed * Time.deltaTime;
        }

        float scroll = Input.GetAxis("Mouse ScrollWheel");
        pos.z += scroll * ScrollSpeed * 100f * Time.deltaTime;

        pos.x = Mathf.Clamp(pos.x, -panLimitX, panLimitX);
        pos.y = Mathf.Clamp(pos.y, -panLimitY, panLimitY);
        pos.z = Mathf.Clamp(pos.z, cameraZoomMin, cameraZoomMax); ;

        transform.position = pos; 
	}
}
