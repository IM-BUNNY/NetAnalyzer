#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isVowel(char c) 
{
    c = tolower(c);
    return (c=='a' || c=='e' || c=='i' || c=='o' || c=='u');
}

int main() 
{
    char word[100];
    char choice;
    int i, len;

    do 
    {
        i = 0;

        printf("\nEnter a word: ");
        scanf("%s", word);

        len = strlen(word);

        if (len == 1) 
        {
            printf("Pig Latin: %s\n", word);
        }

        else if (tolower(word[0]) == 'y' && !isVowel(word[1])) 
        {
            printf("Pig Latin: %syay\n", word);
        }

        else if (isVowel(word[0])) 
        {
            printf("Pig Latin: %syay\n", word);
        }

        else 
        {
            while (i < len) 
            {
                if (isVowel(word[i])) 
                {
                    if (i > 0 && tolower(word[i]) == 'u' && tolower(word[i - 1]) == 'q') 
                    {
                        i++;
                        continue;
                    }
                    break;
                }
                i++;
            }

            printf("Pig Latin: ");
            printf("%s", word + i); 

            for (int j = 0; j < i; j++)
                printf("%c", word[j]);

            printf("ay\n");
        }

        printf("\nDo you want to enter another word ? (y/n): ");
        scanf(" %c", &choice);

    } 
    while (choice == 'y' || choice == 'Y');

    printf("\nThank you\n");
    return 0;
}