using UnityEngine;

public class disableObjectTimer : MonoBehaviour
{
    // Time delay before turning off the GameObject
    public float delayTime = 2f;

    // Variable to keep track of time elapsed
    private float elapsedTime = 0f;

    // Boolean to check if the countdown has started
    private bool isCounting = false;

    void Start()
    {
        // Uncomment the following line if you want to start the countdown immediately at game start
        //StartCountdown();
    }

    void OnEnable()
    {
        // Start the countdown when the GameObject is enabled
        StartCountdown();
    }

    void Update()
    {
        // Check if countdown has started
        if (isCounting)
        {
            // Increment elapsed time
            elapsedTime += Time.deltaTime;

            // Check if elapsed time has exceeded delayTime
            if (elapsedTime >= delayTime)
            {
                // Turn off the GameObject
                gameObject.SetActive(false);

                // Reset variables
                elapsedTime = 0f;
                isCounting = false;
            }
        }
    }

    // Method to start the countdown
    public void StartCountdown()
    {
        // Reset elapsed time and start counting
        elapsedTime = 0f;
        isCounting = true;
    }

    // Method to stop the countdown
    public void StopCountdown()
    {
        // Stop counting
        isCounting = false;
    }
}
