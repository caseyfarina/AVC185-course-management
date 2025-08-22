using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class _raceTimer : MonoBehaviour
{
    private bool startTimerBool = false;
    private float timerTime = 0f;
    public TMP_Text timerText;
    private float minutes = 0;
    private float seconds = 0;
   

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (startTimerBool)
        {
            timerTime += Time.deltaTime;

            minutes = Mathf.FloorToInt(timerTime / 60);
            seconds = Mathf.FloorToInt(timerTime % 60);


            timerText.text = string.Format("{0:00}:{1:00}", minutes, seconds);


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


}
