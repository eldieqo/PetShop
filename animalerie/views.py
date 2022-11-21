from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

# List que contien les animals et equipements sauvargadé!
def animal_list(request):
    animals = Animal.objects.all()
    equipement = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {'animals': animals, 'equipement': equipement})


def verification_animal(id_animal):
    if Animal.objects.filter(pk=id_animal).exists():
        return None
    else:
        print("Désolé " + id_animal+ " n'est pas un équipement connu")
        return None


def change_etat(nouveau_lieu, animal, ancien_lieu):
    authorized_states={'affamé','fatigué','repus','endormi'}
    if animal.etat in authorized_states:
        if nouveau_lieu.id_equip == "mangeoire":
            ancien_lieu.disponibilite = "libre"
            animal.etat = "repus"

        elif nouveau_lieu.id_equip == "roue":
            ancien_lieu.disponibilite = "libre"
            animal.etat = "fatigué"

        elif nouveau_lieu.id_equip == "nid":
            ancien_lieu.disponibilite = "libre"
            animal.etat = "endormi"

        elif nouveau_lieu.id_equip == "litière":
            ancien_lieu.disponibilite = "libre"
            animal.etat = "affamé"
    animal.save()
    ancien_lieu.save()


def change_lieu(nouveau_lieu, ancien_lieu, animal, form):
        error = None
        if nouveau_lieu.id_equip == ancien_lieu.id_equip:
            message = "Félicitations... votre modification a été fait avec success"
            error = True
            return error, nouveau_lieu, ancien_lieu, animal, form, message
        else:
            if (nouveau_lieu.id_equip == "litière"):
                change_etat(nouveau_lieu, animal, ancien_lieu)
                animal.lieu.id_equip = "litière"
                nouveau_lieu.disponibilite = "libre"
                animal.save()
                nouveau_lieu.save()
                form.save() 
                message = "Félicitations... votre modification a été fait avec success"
                error = False
                return error, nouveau_lieu, ancien_lieu, animal, form, message
            else:
                if nouveau_lieu.disponibilite == "occupé":
                    message = "Erreur... essayez à nouveau"
                    error = True
                    return error, nouveau_lieu, ancien_lieu, animal, form, message
                else:
                    change_etat(nouveau_lieu, animal, ancien_lieu)
                    animal.lieu.id_equip = nouveau_lieu.id_equip
                    nouveau_lieu.disponibilite = "occupé"
                    animal.save()
                    nouveau_lieu.save()
                    form.save() 
                    message = "Félicitations... votre modification a été fait avec success"
                    error = False
                    return error, nouveau_lieu, ancien_lieu, animal, form, message


def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal) #Obtien le nom du animal
    message = ""
    form = MoveForm(request.POST, instance=animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip) #Obtien le lieu avant le changement
    verification_animal(animal)
    if request.method == "POST" and form.is_valid():
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)  #Obtien le lieu
        error, nouveau_lieu, ancien_lieu, animal, form, message= change_lieu(nouveau_lieu, ancien_lieu, animal, form)
        return render(request,
            'animalerie/animal_detail.html',
            {'animal': animal, 'message': message, 'error': error, 'lieu': ancien_lieu, 'new_lieu':nouveau_lieu, 'form': form})
    else:
        form = MoveForm()
        return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'message': message, 'lieu': ancien_lieu, 'form': form})







