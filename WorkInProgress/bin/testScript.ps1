[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true } 

#$srv='swdcfrpbi464' #'swbcfrpbi862' #'swdcfrpbi786'
$wsi='ReportServer' #'ReportServer_MWBPBI01' #ReportServer_MWDPBI01
#$url='http://' + $srv + '/' + $wsi
$pathFolder='C:\Users\celerierma\OneDrive - Groupe BPCE\00-PROJETS\04-PBI\RIFA\WorkInProgress'

#Arreter le script en cas d'erreur
#$ErrorActionPreference = "Stop"

# TODO : Gestion des users technique en fonction des environnements
# Ici est pris compte uniquement le user technique de DEV
# La recherche du de l'environnement sera par liste des serveurs fournit
# A ECRIRE ==> foreach ($srv in $liste_srvs){}

$pbiServers = get-Content -path $pathFolder'\InfoserveurZabbix.txt'

function Get-Environment {
	Param ([string]$env)
	if (($env -eq "d") -or ($env -eq "D"))
		{$env = "Dev"}
	elseif (($env -eq "u") -or ($env -eq "U") -or ($env -eq "t")  -or ($env -eq "T"))
		{$env = "Rec"}
	elseif (($env -eq "b") -or ($env -eq "B") -or ($env -eq "q")  -or ($env -eq "Q"))
		{$env = "Qualif"}
	elseif (($env -eq "p") -or ($env -eq "P"))
		{$env = "Prod"}

	return $env
}

foreach ($srv in $pbiServers){
	
	write-host "<======================================>"
	write-host $srv

	$url='http://' + $srv + '/' + $wsi
	$pathFileUri=$srv + '.html'
	write-host $url
	
	$password = ConvertTo-SecureString '!6@7Ck7!Bl7Gi7C' -AsPlainText -Force
	# URL Production: #GET https://security.api.intranatixis.com/security/password_vault/v1/getAccount?safeName={safeName}&accountName={accountName}
	# 		GET https://security.api.intranatixis.com/security/password_vault/v1/getAccount?safeName=CF-PRD-IFA-MDW&accountName=idpbiproc
	$credential = New-Object System.Management.Automation.PSCredential('idpbiproc',$password)
	$outFileUri = $pathFolder + "\" + $pathFileUri
	
	try{
		$response = Invoke-WebRequest -Uri $url -Credential $credential -OutFile $outFileUri
		$statuscode = $response.StatusCode
        $StatusDescription = $response.StatusDescription
        write-host "statusCode : " $statuscode
        Write-Host "StatusDescription : " $StatusDescription
        
	} catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        $StatusDescription = $_.Exception.Response.StatusDescription
        $Exception=$_.Exception
        if (($Exception -match "Impossible de se connecter au serveur distant")){
            write-host "Fais chier: " $srv
            
        }
        write-host "statusCode ERR : " $statuscode
        Write-Host "StatusDescription ERR : " $StatusDescription
    }


	# Gestion du code retour Invoke-WebRequest

}
