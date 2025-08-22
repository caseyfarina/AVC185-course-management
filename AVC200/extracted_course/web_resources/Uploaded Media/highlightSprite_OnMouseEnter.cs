using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class highlightSprite_OnMouseEnter : MonoBehaviour
{

    SpriteRenderer thisSprite;
    public Color tintColor = Color.green;
    Color originalColor;
    // Start is called before the first frame update
    void Start()
    {
        thisSprite = GetComponent<SpriteRenderer>();

        if(thisSprite != null)
        {
            originalColor = thisSprite.color;
            Debug.Log(originalColor);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }

     void OnMouseEnter()
    {
        thisSprite.color = tintColor;
    }

     void OnMouseExit()
    {
        thisSprite.color = originalColor;
    }
}
