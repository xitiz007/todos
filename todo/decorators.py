from django.shortcuts import redirect

def user_not_logged_in(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        return view_function(request, *args, **kwargs)
    return wrapper_function