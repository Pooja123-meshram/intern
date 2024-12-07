from django.shortcuts import render, get_object_or_404
from signUp.models import CustomUser
from services.models import Service, Service_page
from profiles.models import UserProfile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from admin_customization.models import HeroSection, WorkStep, ContactInfo
from examination.models import Test

# from django.shortcuts import render, get_object_or_404

@login_required
def layout_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    except UserProfile.DoesNotExist:
        profile_image_url=None 

    user_online = request.user.is_online()

    

    return render(request, 'main/Layout.html', {
        'profile_image_url': profile_image_url,
        'user_online': user_online,
    })
    
def home_view(request ):
    

    try:
        
        users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
        services = Service.objects.all()
        paginator = Paginator(services, 6)  # Paginate after fetching services
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        service_pages = Service_page.objects.all()

        # Fetch HeroSection, WorkStep, and ContactInfo
        hero_section = HeroSection.objects.first()
        work_steps = WorkStep.objects.all()
        contact_info = ContactInfo.objects.first()
        
        profile_image_url = None
        # Check if the user is authenticated before querying the profile
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
            except UserProfile.DoesNotExist:
                profile_image_url = None
        

        # Fetch top 5 candidates by score
        top_candidates = Test.objects.order_by('-score')[:5]
        

        return render(request, 'main/Index.html', {
            'users': users,
            'profile_image_url': profile_image_url,
            'services': services,  # Services might not be necessary since you already have page_obj
            'page_obj': page_obj,
            'hero_section': hero_section,
            'work_steps': work_steps,
            'contact_info': contact_info,
            'service_pages':service_pages,

            'top_candidates': top_candidates,  # add 
            
        })
    except UnicodeDecodeError:
        return render(request, 'main/error.html', {'error_message': 'UnicodeDecodeError occurred'})
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)






# def candidate_list(request):
#     # Fetch only users with the role of 'candidate'
#     c=UserProfile.objects.all()
#     print(c)
#     users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
#     services = Service.objects.all()
#     print(users)
#     print(services)
#     candidates = CustomUser.objects.filter(role='candidate')
#     for i in candidates:
#         print(i.username,i.first_name)
#     # Render the candidates in a template
#     return render(request, 'main/candidate_list.html', {'candidates': candidates})

def candidate_list(request):
    """View to list all candidates."""
    try:
        # Fetch paginated services
        services = Service.objects.all()
        paginator = Paginator(services, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Fetch other required data
        hero_section = HeroSection.objects.first()
        work_steps = WorkStep.objects.all()
        contact_info = ContactInfo.objects.first()

        profile_image_url = None
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
            except UserProfile.DoesNotExist:
                profile_image_url = None

        # Fetch all candidates
        all_candidates = CustomUser.objects.filter(role='candidate')
        

        return render(request, 'main/candidate_list.html', {
            'profile_image_url': profile_image_url,
            'services': services,
            'page_obj': page_obj,
            'hero_section': hero_section,
            'work_steps': work_steps,
            'contact_info': contact_info,
            'service_pages': Service_page.objects.all(),
            'all_candidates': all_candidates,
        })
    except UnicodeDecodeError:
        return render(request, 'main/error.html', {'error_message': 'UnicodeDecodeError occurred'})