using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class linearMovement : MonoBehaviour
{


    [Header("Initial State")]
    public bool toggleActive = true;

    [Space(10)] // 10 pixels of spacing here.
    [Header("Movement(translation) Speed Per Axis")]
    [Range(-10f, 10f)]
    public float xSpeed = 1f;
    [Range(-10f, 10f)]
    public float ySpeed = 0f;
    [Range(-10f, 10f)]
    public float zSpeed = 0f;

    [Header("Percentage of Randomness")]
    [Range(0f, 1f)]
    public float randomPercentage= .1f;

    [Header("Check box for object space")]
    public bool objectSpace = false;
    private Vector3 direction;
    private float directionMultiplier = 0f;
    private void Start()
    {
        direction = new Vector3(
                xSpeed + Random.Range(-(xSpeed * randomPercentage), (xSpeed * randomPercentage)),
                ySpeed + Random.Range(-(ySpeed * randomPercentage), (ySpeed * randomPercentage)),
                zSpeed + Random.Range(-(zSpeed * randomPercentage), (zSpeed * randomPercentage))
                );
    }
    // Update is called once per frame
    void Update()
    {

        // this line translates the gameboject in a direction
        if (objectSpace)
        {
            transform.Translate(direction * (Time.deltaTime),Space.Self);
        }
        else
        {
            transform.Translate(direction * (Time.deltaTime), Space.World);
        }
        
       
    }
}
