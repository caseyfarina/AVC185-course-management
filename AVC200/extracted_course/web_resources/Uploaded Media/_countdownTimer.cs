


using UnityEngine;
using TMPro;
using UnityEngine.Events;

public class _countdownTimer : MonoBehaviour
{
    [SerializeField]
    private float maxTimeInSeconds = 60.0f; // Maximum time in seconds (adjustable in the editor)

    [SerializeField]
    private TextMeshProUGUI timerText; // Reference to the TextMeshPro text field

    [SerializeField]
    private UnityEvent onTimerEnd; // Unity event to be invoked when the timer reaches zero

    private float currentTimeInSeconds;

    private void Start()
    {
        currentTimeInSeconds = maxTimeInSeconds;
        UpdateTimerText();
    }

    private void Update()
    {
        if (currentTimeInSeconds > 0)
        {
            currentTimeInSeconds -= Time.deltaTime;

            if (currentTimeInSeconds <= 0)
            {
                currentTimeInSeconds = 0;
                TimerEnd();
            }

            UpdateTimerText();
        }
    }

    private void UpdateTimerText()
    {
        if (timerText != null)
        {
            timerText.text = currentTimeInSeconds.ToString("F1"); // Format time with one decimal place
        }
    }

    private void TimerEnd()
    {
        // Timer has reached zero, invoke the Unity event
        if (onTimerEnd != null)
        {
            onTimerEnd.Invoke();
        }
    }
}
