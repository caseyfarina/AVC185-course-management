using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

// Quits the player when the user hits escape

public class _escapeToQuit : MonoBehaviour
{
	
    void Update()
    {
        if (Input.GetKey("escape"))
        {
            Application.Quit();
        }

	
    }
}
