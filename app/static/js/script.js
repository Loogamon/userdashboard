function delete_this(id,who,debug)
{
	if (confirm("Are you sure about deleting "+who+"?"))
	{
		window.location.href = "/users/delete/"+id
		if (debug)
			window.location.href = "/users/delete/"+id+"?q=debug"
	}
}