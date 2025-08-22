using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Cinemachine;

public class avoidanceGameManager : MonoBehaviour
{
    public GameObject player;
    public GameObject spawnPoint;
    public GameObject Start_text;
    public GameObject Win_text;
    public GameObject Lose_text;
    public GameObject GoalPoint;
    public CinemachineVirtualCamera cmVcam1; 


    private playerInteraction interactionData;
    private GameObject currentPlayer;
   


    // Start is called before the first frame update
    void Start()
    {
        if (Start_text != null)
        {
            Start_text.SetActive(true);
        }
        Invoke("turnOffText", 2);


        //create the player
        currentPlayer = Instantiate(player, spawnPoint.transform.position, Quaternion.identity);
        if (cmVcam1 != null) { cmVcam1.Follow = currentPlayer.transform; }
            //store the players hit information
        interactionData = currentPlayer.GetComponent<playerInteraction>();
    }

    // Update is called once per frame
    void Update()
    {
        if (interactionData.runOver)
        {
            interactionData.runOver = false;
            //destroy the player that got hit
            Destroy(currentPlayer);

            if (Lose_text != null) { Lose_text.SetActive(true); }
            
            Invoke("turnOffText", 2);

            Invoke("createNewPlayer", 1f);
           
        }

        if (interactionData.achievedGoal)
        {
            if (Win_text != null){ Win_text.SetActive(true);}

            currentPlayer.GetComponent<movementArcade>().enabled = false;
            currentPlayer.GetComponent<Collider2D>().enabled = false;

        }
    }

    void turnOffText()
    {
        if (Win_text & Start_text & Lose_text != null)
        {
            Start_text.SetActive(false);
            Win_text.SetActive(false);
            Lose_text.SetActive(false);
        }
    }

    void createNewPlayer()
    {
        //create a new player at the starting spawn point

        currentPlayer = Instantiate(player, spawnPoint.transform.position, Quaternion.identity);
        //store the player hit information again
        interactionData = currentPlayer.GetComponent<playerInteraction>();
        if (cmVcam1 != null) { cmVcam1.Follow = currentPlayer.transform; }
        interactionData.runOver = false;


    }


}
