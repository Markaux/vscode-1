[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true } 

#$srv='swdcfrpbi464' #'swbcfrpbi862' #'swdcfrpbi786'
$wsi='ReportServer' #'ReportServer_MWBPBI01' #ReportServer_MWDPBI01
#$url='http://' + $srv + '/' + $wsi
$pathFolder='C:\Users\celerierma\OneDrive - Groupe BPCE\00-PROJETS\04-PBI\RIFA'
$transcript=$pathFolder + '\transcript.txt'

#Arreter le script en cas d'erreur
#$ErrorActionPreference = "Stop"

#Logs les infos du script
Start-Transcript -Path $transcript 

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
	} catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
    }
	write-host $statuscode

	# Gestion du code retour Invoke-WebRequest
	
	
	$ver=Get-Content -Path $pathFileUri
	foreach ($line in $ver){
		#Write-Host "La ligne est : " $line
		if (($line -match "cfr") -and ($line -match "title")){
			$application_iua = $line.substring(17,3).toupper()
			$environment = Get-Environment($line.substring(13,1))
			$server = $line.substring(11,12).toupper()
			$technical_iua = "PBI".toupper()
			$application_version = ""
		}
		
		if (($line -match "Microsoft Power BI Report Server Version ") -and ($line -notmatch "meta")){
			#Write-Host "La ligne est : " $line
			$ligne_splitted=$line.split(" ")
			$technical_version = $ligne_splitted[6]
		}
	}

	### Check des variables
	Write-Host "application_iua : " $application_iua
	Write-Host "environment : " $environment
	Write-Host "server : " $server
	Write-Host "technical_iua : " $technical_iua
	Write-Host "technical_version : " $technical_version
	Write-Host "application_version : "	$application_version

	#### Formattage du fichier json
	## sous la forme $technical_iua_$application_iua_$server_$environment.json
	$pathFileJson = $pathFolder + '\' + $technical_iua + '_' + $application_iua + '_' + $server + '_' + $environment + '.json'
	$jsonfile = '{"data": [{"application_iua":"' + $application_iua + '","environment":"' + $environment + '","server":"' + $server + '","technical_iua":"' + $technical_iua + '","technical_version":"' + $technical_version + '","application_version":"' + $application_version + '","technical_version_details":""}]}'

	$jsonfile | set-content -path $pathFileJson
}
