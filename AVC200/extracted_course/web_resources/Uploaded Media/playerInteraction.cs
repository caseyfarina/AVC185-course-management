using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class playerInteraction : MonoBehaviour
{
    public string enemyTag = "enemy";
    public string goalTag = "goal";

    private Transform startingPosition;

    public bool runOver = false;
    public bool achievedGoal = false;
 
    // Start is called before the first frame update
    void Start()
    {
        startingPosition = gameObject.transform;

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.CompareTag(enemyTag))
        {

            runOver = true;
     
        }

        if (collision.gameObject.CompareTag(goalTag))
        {

            achievedGoal = true;
            print("win");
        }

    }

}
