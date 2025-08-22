using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.Events;

public class _raceCountDownTimer : MonoBehaviour
{
    private bool startTimerBool = false;
    public float timerTime = 10f;
    public TMP_Text timerText;
    private float minutes = 0;
    private float seconds = 0;

    public UnityEvent timeOutEvent;
    public float bonusTimeAmount = 10f; 
   

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        timerTime = Mathf.Clamp(timerTime, 0f, 1000000);
        if (startTimerBool)
        {
            //calculate time independent of framerate
            // time = time - second
            timerTime -= Time.deltaTime;
            timerTime = Mathf.Clamp(timerTime, 0f, 1000000);
            minutes = Mathf.FloorToInt(timerTime / 60);
            seconds = Mathf.FloorToInt(timerTime % 60);

            
            timerText.text = string.Format("{0:00}:{1:00}", minutes, seconds);
            

        }


        if(timerTime <= 0f)
        {
            timeOutEvent?.Invoke();
        }
    }
   

    public void startTimer()
    {
        startTimerBool = true;
    }

    public void stopTimer()
    {
        startTimerBool = false;
    }

    public void addToTime()
    {

      //  timerTime = timerTime + bonusTimeAmount;

        timerTime += bonusTimeAmount;
    }


}
