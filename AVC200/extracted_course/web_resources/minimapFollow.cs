using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class minimapFollow : MonoBehaviour
{
    public GameObject botBody;

    private Vector3 offset;
    // Start is called before the first frame update
    void Start()
    {
        offset = transform.position - botBody.transform.position;
    }

    // Update is called once per frame
    void Update()
    {


        //float yoffset = transform.position.y;
        //Vector3 displacePosition = new Vector3(botBody.transform.position.x, yoffset + botBody.transform.position.y, botBody.transform.position.z);
        transform.position = botBody.transform.position + offset;



    }
}
