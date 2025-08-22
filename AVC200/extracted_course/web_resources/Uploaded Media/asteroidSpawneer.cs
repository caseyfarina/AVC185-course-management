using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class asteroidSpawneer : MonoBehaviour
{

    public GameObject[] asteroidPrefabs;

    public float secondsPerAsteroid = 5f;

    public float xPosition = 38f;
    public float yPosition = 24f;

    //public Vector3 spawnPosition;


    // Start is called before the first frame update
    void Start()
    {
        Invoke("spawnAsteroid", secondsPerAsteroid);
    }

    // Update is called once per frame
    void Update()
    {

      
    }

    void spawnAsteroid()
    {
        //pick a random corner
        Vector3 spawnPosition = new Vector3(xPosition, yPosition, 0f); 

        float randomChoice = Random.Range(0, 3);

        if (randomChoice == 0 )
        {
            spawnPosition = new Vector3(xPosition, yPosition, 0f);
        }

        if( randomChoice == 1)
        { 
            spawnPosition = new Vector3(-xPosition, yPosition, 0f);
        }


        if (randomChoice == 2)
        {
            spawnPosition = new Vector3(xPosition, -yPosition, 0f);
        }

        if (randomChoice == 3)
        {
            spawnPosition = new Vector3(-xPosition, -yPosition, 0f);
        }

        //randomly select a prefab
        int prefabNumber = Random.Range(0, asteroidPrefabs.Length);


        //make a new asteroid
        Instantiate(asteroidPrefabs[prefabNumber], spawnPosition, transform.rotation);

        //make another asteroid
        if(gameObject.activeSelf == true)
        {
            Invoke("spawnAsteroid", secondsPerAsteroid);
        }
           
    }


}
